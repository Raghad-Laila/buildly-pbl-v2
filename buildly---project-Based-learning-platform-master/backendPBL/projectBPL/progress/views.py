from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.views import (
    IsCourseInstructor,
    get_accessible_project_or_404,
)
from progress.models import ProjectProgress
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from account.notifications import (
    create_project_graded_notification,
    create_project_submitted_notification,
)

class UserProjectProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        progresses = ProjectProgress.objects.filter(user=request.user)

        data = {
            p.project.id: {
                'status': p.status,
                'started_at': p.started_at,
                'completed_at': p.completed_at,
            }
            for p in progresses
        }

        return Response(data)

class CompleteProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        project = get_accessible_project_or_404(request.user, project_id)

        progress, created = ProjectProgress.objects.get_or_create(
            user=request.user,
            project=project,
        )

        was_already_completed = progress.status == 'completed'
        
        progress.status = 'completed'
        progress.progress_percentage = 100
        progress.completed_at = timezone.now()
        progress.save()

        if not was_already_completed:
            create_project_submitted_notification(user=request.user, project=project)
        
        return Response({'status': 'project completed successfully'})
    
class ProjectProgressDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        progress = get_object_or_404(ProjectProgress, user=request.user, project_id=project_id)
        
        duration = None
        if progress.started_at and progress.completed_at:
            diff = progress.completed_at - progress.started_at
            duration = round(diff.total_seconds() / 60) 

        return Response({
            'status': progress.status,
            'started_at': progress.started_at,
            'completed_at': progress.completed_at,
            'duration_minutes': duration,
            'progress_percentage': progress.progress_percentage
        })
    

class AdminProjectSubmissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def get(self, request, project_id):
        submissions = ProjectProgress.objects.filter(
            project_id=project_id, 
            status='completed'
        ).select_related('user').order_by('-completed_at')

        data = [{
            'id': s.id,
            'user_id': s.user.id,
            'user_email': s.user.email,
            'completed_at': s.completed_at,
            'is_graded': s.is_graded,
            'grade_stars': s.grade_stars,
            'feedback': s.feedback,
            'progress_percentage': s.progress_percentage
        } for s in submissions]

        return Response(data)
    
class AdminProjectReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def post(self, request, project_id):
        user_id = request.data.get('userId')
        stars = request.data.get('stars')
        overall_feedback = request.data.get('feedback')

        if not user_id or stars is None:
            return Response({'error': 'userId and stars are required'}, status=status.HTTP_400_BAD_REQUEST)

        progress = get_object_or_404(
            ProjectProgress.objects.select_related('user', 'project'),
            project_id=project_id,
            user_id=user_id,
        )

        progress.grade_stars = stars
        progress.feedback = overall_feedback
        progress.is_graded = True
        progress.save()

        create_project_graded_notification(user=progress.user, project=progress.project)

        return Response({
            'message': 'Final project review submitted successfully',
            'project_id': project_id,
            'user_id': user_id,
            'stars': stars
        })
    
class AdminSingleSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def get(self, request, project_id, user_id):
        submission = get_object_or_404(
            ProjectProgress, 
            project_id=project_id, 
            user_id=user_id,
            status='completed'
        )

        data = {
            'id': submission.id,
            'user_id': submission.user.id,
            'is_graded': submission.is_graded,
            'grade_stars': submission.grade_stars,
            'feedback': submission.feedback,
            'completed_at': submission.completed_at
        }

        return Response(data)
