from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course

from .adaptive import apply_answer, get_starting_question, select_next_question
from .constants import (
    INITIAL_ABILITY_SCORE,
    TOTAL_QUESTIONS,
    ability_to_final_level,
    is_frontend_placement_course,
)
from .models import PlacementAttempt, PlacementQuestion
from .serializers import (
    PlacementAnswerSerializer,
    PlacementQuestionPublicSerializer,
    PlacementStartSerializer,
    PlacementStatusSerializer,
)


class IsLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_learner)


def serialize_question(question):
    return PlacementQuestionPublicSerializer(question).data


def get_current_question(attempt):
    answered_ids = {response['question_id'] for response in attempt.responses}
    for question_id in reversed(attempt.asked_question_ids):
        if question_id not in answered_ids:
            return PlacementQuestion.objects.filter(id=question_id, is_active=True).first()
    return None


def build_status_payload(user, course):
    completed_attempt = PlacementAttempt.objects.filter(
        user=user,
        course=course,
        status='completed',
    ).first()
    in_progress_attempt = PlacementAttempt.objects.filter(
        user=user,
        course=course,
        status='in_progress',
    ).first()

    return {
        'requires_placement': is_frontend_placement_course(course),
        'has_completed': bool(completed_attempt),
        'has_in_progress': bool(in_progress_attempt),
        'attempt_id': in_progress_attempt.id if in_progress_attempt else None,
        'ability_score': completed_attempt.ability_score if completed_attempt else None,
        'final_level': completed_attempt.final_level if completed_attempt else None,
        'final_level_display': completed_attempt.get_final_level_display()
        if completed_attempt and completed_attempt.final_level
        else None,
        'completed_at': completed_attempt.completed_at if completed_attempt else None,
        'is_enrolled': course.is_student_enrolled(user),
    }


def finalize_attempt(attempt, user):
    attempt.ability_score = round(attempt.ability_score, 2)
    attempt.final_level = ability_to_final_level(attempt.ability_score)
    attempt.status = 'completed'
    attempt.completed_at = timezone.now()
    attempt.save(
        update_fields=['ability_score', 'final_level', 'status', 'completed_at']
    )

    user.level = attempt.final_level
    user.is_rated = True
    user.save(update_fields=['level', 'is_rated'])

    if not attempt.course.is_student_enrolled(user):
        attempt.course.add_learner(user)

    return attempt


class FrontendPlacementStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLearner]

    def get(self, request, course_id):
        course = Course.objects.filter(id=course_id, is_active=True).first()
        if not course:
            return Response({'error': 'المسار غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        payload = build_status_payload(request.user, course)
        serializer = PlacementStatusSerializer(payload)
        return Response(serializer.data)


class FrontendPlacementStartView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLearner]

    def post(self, request):
        serializer = PlacementStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = Course.objects.filter(
            id=serializer.validated_data['course_id'],
            is_active=True,
        ).first()
        if not course:
            return Response({'error': 'المسار غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        if not is_frontend_placement_course(course):
            return Response(
                {'error': 'اختبار تحديد المستوى متاح لمسار Frontend فقط'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if course.is_student_enrolled(request.user):
            return Response(
                {'error': 'أنت منضم بالفعل لهذا المسار'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        completed_attempt = PlacementAttempt.objects.filter(
            user=request.user,
            course=course,
            status='completed',
        ).first()
        if completed_attempt:
            if not course.is_student_enrolled(request.user):
                course.add_learner(request.user)
            return Response(
                {
                    'completed': True,
                    'attempt_id': completed_attempt.id,
                    'ability_score': completed_attempt.ability_score,
                    'final_level': completed_attempt.final_level,
                    'final_level_display': completed_attempt.get_final_level_display(),
                    'completed_at': completed_attempt.completed_at,
                    'enrolled': True,
                }
            )

        attempt = PlacementAttempt.objects.filter(
            user=request.user,
            course=course,
            status='in_progress',
        ).first()

        if attempt and attempt.questions_answered >= attempt.total_questions:
            finalize_attempt(attempt, request.user)
            return Response(
                {
                    'completed': True,
                    'attempt_id': attempt.id,
                    'ability_score': attempt.ability_score,
                    'final_level': attempt.final_level,
                    'final_level_display': attempt.get_final_level_display(),
                    'completed_at': attempt.completed_at,
                    'enrolled': True,
                }
            )

        if not attempt:
            if PlacementQuestion.objects.filter(is_active=True).count() < TOTAL_QUESTIONS:
                return Response(
                    {'error': 'بنك الأسئلة غير جاهز بعد. تواصل مع المشرف.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            first_question = get_starting_question()
            if not first_question:
                return Response(
                    {'error': 'لا توجد أسئلة متاحة لبدء الاختبار'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            attempt = PlacementAttempt.objects.create(
                user=request.user,
                course=course,
                ability_score=INITIAL_ABILITY_SCORE,
                asked_question_ids=[first_question.id],
                total_questions=TOTAL_QUESTIONS,
            )
            current_question = first_question
        else:
            current_question = get_current_question(attempt)
            if not current_question:
                first_question = get_starting_question()
                if not first_question:
                    return Response(
                        {'error': 'لا توجد أسئلة متاحة لاستئناف الاختبار'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )
                attempt.asked_question_ids.append(first_question.id)
                attempt.save(update_fields=['asked_question_ids'])
                current_question = first_question

        return Response(
            {
                'attempt_id': attempt.id,
                'total_questions': attempt.total_questions,
                'current_question_number': attempt.questions_answered + 1,
                'ability_score': attempt.ability_score,
                'question': serialize_question(current_question),
            }
        )


class FrontendPlacementSubmitAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLearner]

    def post(self, request):
        serializer = PlacementAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        attempt = PlacementAttempt.objects.filter(
            id=data['attempt_id'],
            user=request.user,
            status='in_progress',
        ).select_related('course').first()

        if not attempt:
            return Response({'error': 'محاولة الاختبار غير موجودة'}, status=status.HTTP_404_NOT_FOUND)

        question = PlacementQuestion.objects.filter(
            id=data['question_id'],
            is_active=True,
        ).first()
        if not question:
            return Response({'error': 'السؤال غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        if question.id not in attempt.asked_question_ids:
            return Response({'error': 'هذا السؤال ليس ضمن الاختبار الحالي'}, status=status.HTTP_400_BAD_REQUEST)

        if attempt.responses and attempt.responses[-1].get('question_id') == question.id:
            return Response({'error': 'تمت الإجابة على هذا السؤال مسبقاً'}, status=status.HTTP_400_BAD_REQUEST)

        is_correct = data['selected_answer'] == question.correct_answer
        attempt.ability_score = apply_answer(attempt.ability_score, is_correct)
        attempt.responses.append(
            {
                'question_id': question.id,
                'topic': question.topic,
                'selected_answer': data['selected_answer'],
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'time_ms': data.get('time_ms', 0),
                'ability_after': attempt.ability_score,
            }
        )
        attempt.save(update_fields=['ability_score', 'responses'])

        answered_count = attempt.questions_answered
        response_payload = {
            'is_correct': is_correct,
            'explanation': question.explanation,
            'ability_score': attempt.ability_score,
            'current_question_number': answered_count,
            'completed': False,
        }

        if answered_count >= attempt.total_questions:
            attempt = finalize_attempt(attempt, request.user)
            response_payload.update(
                {
                    'completed': True,
                    'final_level': attempt.final_level,
                    'final_level_display': attempt.get_final_level_display(),
                    'completed_at': attempt.completed_at,
                    'enrolled': True,
                }
            )
            return Response(response_payload)

        used_ids = attempt.asked_question_ids
        asked_questions = list(
            PlacementQuestion.objects.filter(id__in=used_ids)
        )
        next_question = select_next_question(
            attempt.ability_score,
            used_ids,
            asked_questions,
        )

        if not next_question:
            attempt = finalize_attempt(attempt, request.user)
            response_payload.update(
                {
                    'completed': True,
                    'final_level': attempt.final_level,
                    'final_level_display': attempt.get_final_level_display(),
                    'completed_at': attempt.completed_at,
                    'enrolled': True,
                }
            )
            return Response(response_payload)

        attempt.asked_question_ids.append(next_question.id)
        attempt.save(update_fields=['asked_question_ids'])

        response_payload.update(
            {
                'current_question_number': answered_count + 1,
                'question': serialize_question(next_question),
            }
        )
        return Response(response_payload)
