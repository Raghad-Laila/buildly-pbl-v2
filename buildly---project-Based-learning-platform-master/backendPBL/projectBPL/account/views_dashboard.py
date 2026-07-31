# accounts/views_dashboard.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Count, F, Q, Sum
from datetime import timedelta
from .models import CustomUser, UserFavorite, Notification
from .notifications import serialize_notification
from .serializers import ProfileSerializer
from progress.models import ProjectProgress
from projects.models import Project, TaskSubmission
from courses.models import Course

class LearnerDashboardView(APIView):
    """لوحة تحكم المتعلم"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # التحقق من أن المستخدم متعلم
        if not user.is_learner:
            return Response({
                'error': _('هذه اللوحة مخصصة للمتعلمين فقط')
            }, status=status.HTTP_403_FORBIDDEN)
        
        # بيانات الملف الشخصي
        profile_serializer = ProfileSerializer(user)
        
        # الإحصائيات
        stats = self.get_learner_stats(user)
        
        # المسارات التعليمية (المشاريع)
        enrolled_projects = self.get_enrolled_projects(user)
        
        # التقدم التعليمي
        progress = self.get_learning_progress(user)
        
        # الإشعارات والنشاطات
        notifications = self.get_recent_notifications(user)
        recent_activity = self.get_recent_activity(user)
        
        # المشاريع المقترحة
        suggested_projects = self.get_suggested_projects(user, request)
        
        return Response({
            'message': _('لوحة تحكم المتعلم'),
            'user_profile': profile_serializer.data,
            'dashboard_stats': stats,
            'enrolled_projects': enrolled_projects,
            'learning_progress': progress,
            'notifications': notifications,
            'recent_activity': recent_activity,
            'suggested_projects': suggested_projects,
            'quick_actions': self.get_quick_actions(),
        })
    
    def get_learner_stats(self, user):
        """إحصائيات حقيقية من تقدم المشاريع ضمن المسارات النشطة المنضم إليها"""
        enrolled_courses_count = Course.objects.filter(
            enrolled_learners=user,
            is_active=True,
            is_archived=False,
        ).count()

        accessible_projects_qs = Project.objects.filter(
            course__enrolled_learners=user,
            course__is_active=True,
            course__is_archived=False,
            is_active=True,
        )
        accessible_project_ids = accessible_projects_qs.values_list('id', flat=True)

        progress_qs = ProjectProgress.objects.filter(
            user=user,
            project_id__in=accessible_project_ids,
        ).select_related('project')

        completed_projects = progress_qs.filter(status='completed').count()
        in_progress_projects = progress_qs.filter(status='in_progress').count()

        # ساعات التعلم = مجموع مدة المسارات المنضم إليها التي أكمل المتعلم كل مشاريعها النشطة
        completed_courses = Course.objects.filter(
            enrolled_learners=user,
            is_active=True,
            is_archived=False,
        ).annotate(
            active_projects_count=Count(
                'projects',
                filter=Q(projects__is_active=True),
                distinct=True,
            ),
            completed_projects_count=Count(
                'projects',
                filter=Q(
                    projects__is_active=True,
                    projects__projectprogress__user=user,
                    projects__projectprogress__status='completed',
                ),
                distinct=True,
            ),
        ).filter(
            active_projects_count__gt=0,
            active_projects_count=F('completed_projects_count'),
        )

        total_hours_spent = (
            completed_courses.aggregate(
                total=Sum('estimated_duration')
            )['total']
            or 0
        )

        graded = list(
            progress_qs.filter(is_graded=True, grade_stars__isnull=False)
            .values_list('grade_stars', flat=True)
        )
        avg_score = round(sum(graded) / len(graded), 1) if graded else 0

        accessible_projects = accessible_projects_qs.count()
        completion_rate = (
            int(round((completed_projects / accessible_projects) * 100))
            if accessible_projects
            else 0
        )

        return {
            'total_enrolled_projects': enrolled_courses_count,
            'completed_projects': completed_projects,
            'in_progress_projects': in_progress_projects,
            'total_hours_spent': total_hours_spent,
            'current_streak_days': self.get_streak_days(user),
            'skill_level': self.calculate_skill_level(user),
            'completion_rate': completion_rate,
            'avg_project_score': avg_score,
        }

    def get_enrolled_projects(self, user):
        """المشاريع من المسارات المنضم إليها مع حالة التقدم الحقيقية"""
        projects_qs = (
            Project.objects.filter(
                course__enrolled_learners=user,
                course__is_active=True,
                course__is_archived=False,
                is_active=True,
            )
            .select_related('course')
            .order_by('-created_at')
        )

        progress_map = {
            item.project_id: item
            for item in ProjectProgress.objects.filter(user=user, project__in=projects_qs)
        }

        projects = []
        for project in projects_qs[:5]:
            progress = progress_map.get(project.id)
            status = progress.status if progress else 'not_started'
            status_labels = {
                'not_started': 'لم يبدأ',
                'in_progress': 'قيد التنفيذ',
                'completed': 'مكتمل',
            }
            percentage = 100 if status == 'completed' else (
                progress.progress_percentage if progress else 0
            )

            projects.append({
                'id': project.id,
                'project_id': project.id,
                'title': project.title,
                'description': project.description,
                'status': status_labels.get(status, status),
                'progress_percentage': percentage,
                'deadline': None,
                'last_activity': (
                    (progress.completed_at or progress.started_at).strftime('%Y-%m-%d')
                    if progress and (progress.completed_at or progress.started_at)
                    else None
                ),
                'category': project.course.title,
                'difficulty': project.get_level_display(),
                'estimated_hours': project.estimated_time,
                'course_id': project.course_id,
                'course_title': project.course.title,
            })

        total_count = projects_qs.count()
        return {
            'count': len(projects),
            'projects': projects,
            'has_more': total_count > 5,
            'total_count': total_count,
        }

    def get_learning_progress(self, user):
        """تقدم تعليمي حقيقي من سجلات التقدم"""
        progress_qs = ProjectProgress.objects.filter(user=user).select_related('project')
        completed = progress_qs.filter(status='completed').count()

        total_projects = Project.objects.filter(
            course__enrolled_learners=user,
            course__is_active=True,
            course__is_archived=False,
            is_active=True,
        ).count()

        overall = (
            int(round((completed / total_projects) * 100))
            if total_projects
            else 0
        )

        progress_data = []
        for item in progress_qs.order_by('-completed_at', '-started_at')[:6]:
            progress_data.append({
                'project_name': item.project.title,
                'progress': 100 if item.status == 'completed' else (item.progress_percentage or 0),
                'skills_gained': item.project.get_languages_display_list(),
                'time_spent': item.project.estimated_time or 0,
                'last_update': (
                    (item.completed_at or item.started_at).strftime('%Y-%m-%d')
                    if (item.completed_at or item.started_at)
                    else None
                ),
            })

        now = timezone.now()
        monthly_progress = []
        for i in range(5, -1, -1):
            month_start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
            if i == 0:
                month_end = now
            else:
                next_month = (month_start + timedelta(days=32)).replace(day=1)
                month_end = next_month

            month_completed = progress_qs.filter(
                status='completed',
                completed_at__gte=month_start,
                completed_at__lt=month_end,
            )
            hours = sum((p.project.estimated_time or 0) for p in month_completed.select_related('project'))
            monthly_progress.append({
                'month': month_start.strftime('%b'),
                'completed_projects': month_completed.count(),
                'hours_spent': hours,
            })

        recent_completed = progress_qs.filter(
            status='completed',
            completed_at__gte=now - timedelta(days=30),
        ).count()
        older_completed = progress_qs.filter(
            status='completed',
            completed_at__gte=now - timedelta(days=60),
            completed_at__lt=now - timedelta(days=30),
        ).count()

        if recent_completed > older_completed:
            trend = 'تصاعدي'
        elif recent_completed < older_completed:
            trend = 'تنازلي'
        else:
            trend = 'مستقر'

        return {
            'overall_progress_percentage': overall,
            'progress_by_project': progress_data,
            'monthly_progress': monthly_progress,
            'learning_trend': trend,
        }
    
    def get_recent_notifications(self, user):
        """الإشعارات الحديثة من قاعدة البيانات"""
        notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
        return [serialize_notification(item) for item in notifications]
    
    def get_recent_activity(self, user):
        """النشاطات الحديثة من سجلات التقدم والمفضلة"""
        activities = []

        project_progress = (
            ProjectProgress.objects
            .filter(user=user)
            .select_related('project')
        )

        for progress in project_progress:
            project_title = progress.project.title

            if progress.started_at:
                activities.append({
                    'id': f'start-{progress.id}',
                    'action': 'بدء العمل على مشروع',
                    'project': project_title,
                    'timestamp': progress.started_at.isoformat(),
                    'icon': '🚀',
                    'project_id': progress.project_id,
                    'type': 'project_started',
                })

            if progress.completed_at:
                activities.append({
                    'id': f'complete-{progress.id}',
                    'action': 'إكمال مشروع',
                    'project': project_title,
                    'timestamp': progress.completed_at.isoformat(),
                    'icon': '✅',
                    'project_id': progress.project_id,
                    'type': 'project_completed',
                })

            if progress.is_graded and progress.grade_stars is not None and progress.completed_at:
                activities.append({
                    'id': f'grade-{progress.id}',
                    'action': f'استلام تقييم ({progress.grade_stars}★)',
                    'project': project_title,
                    'timestamp': progress.completed_at.isoformat(),
                    'icon': '🏆',
                    'project_id': progress.project_id,
                    'type': 'project_graded',
                })

        task_submissions = (
            TaskSubmission.objects
            .filter(user=user, is_completed=True, completed_at__isnull=False)
            .select_related('project', 'task')
        )

        for submission in task_submissions:
            activities.append({
                'id': f'task-{submission.id}',
                'action': f'إكمال مهمة: {submission.task.title}',
                'project': submission.project.title,
                'timestamp': submission.completed_at.isoformat(),
                'icon': '📝',
                'project_id': submission.project_id,
                'type': 'task_completed',
            })

        favorites = UserFavorite.objects.filter(user=user).order_by('-created_at')[:15]

        for favorite in favorites:
            if favorite.item_type == UserFavorite.ITEM_TYPE_PROJECT:
                project = Project.objects.filter(id=favorite.object_id).first()
                if not project:
                    continue
                title = project.title
                item_label = 'مشروع'
            else:
                course = Course.objects.filter(id=favorite.object_id).first()
                if not course:
                    continue
                title = course.title
                item_label = 'مسار'

            activities.append({
                'id': f'favorite-{favorite.id}',
                'action': f'إضافة {item_label} إلى المفضلة',
                'project': title,
                'timestamp': favorite.created_at.isoformat(),
                'icon': '⭐',
                'type': 'favorite_added',
            })

        activities.sort(key=lambda item: item['timestamp'], reverse=True)
        return activities[:10]
    

    def get_suggested_projects(self, user, request=None):
        """مشاريع حقيقية من مسارات المتعلم، مناسبة لمستواه وغير مكتملة"""

        if not user.is_rated or not user.level:
            return []

        completed_ids = ProjectProgress.objects.filter(
            user=user,
            completed_at__isnull=False,
        ).values_list('project_id', flat=True)

        enrolled_base = Project.objects.filter(
            course__enrolled_learners=user,
            course__is_active=True,
            course__is_archived=False,
            is_active=True,
        ).exclude(id__in=completed_ids).select_related('course')

        projects = list(
            enrolled_base.filter(level=user.level).order_by('-created_at')[:6]
        )

        # إن لم يوجد تطابق بالمستوى، اعرض مشاريع حقيقية من مساراته
        if not projects:
            projects = list(enrolled_base.order_by('-created_at')[:6])

        suggestions = []
        for project in projects:
            languages = project.get_languages_list()
            languages_display = project.get_languages_display_list()
            image_url = None
            if project.image:
                image_url = (
                    request.build_absolute_uri(project.image.url)
                    if request is not None
                    else project.image.url
                )

            suggestions.append({
                'id': project.id,
                'project_id': project.id,
                'title': project.title,
                'description': project.description,
                'category': project.get_language_display(),
                'difficulty': project.get_level_display(),
                'level': project.level,
                'level_display': project.get_level_display(),
                'language': project.language,
                'language_display': project.get_language_display(),
                'languages': languages,
                'languages_display': languages_display,
                'estimated_time': project.estimated_time,
                'course_id': project.course_id,
                'course_title': project.course.title,
                'image': image_url,
                'reason': 'يتناسب مع مستواك الحالي',
            })

        return suggestions
    
    def get_quick_actions(self):
        """الإجراءات السريعة"""
        return [
            {
                'id': 1,
                'title': 'بدء مشروع جديد',
                'icon': '➕',
                'action': 'start_project',
                'description': 'اختر مشروعًا وابدأ العمل',
            },
            {
                'id': 2,
                'title': 'متابعة المشاريع',
                'icon': '📋',
                'action': 'continue_projects',
                'description': 'استكمل مشاريعك النشطة',
            },
            {
                'id': 3,
                'title': 'مراجعة التقدم',
                'icon': '📊',
                'action': 'review_progress',
                'description': 'راجع إحصائيات تقدمك',
            },
            {
                'id': 4,
                'title': 'طلب مساعدة',
                'icon': '💬',
                'action': 'request_help',
                'description': 'تواصل مع المشرفين',
            },
        ]
    
    # === دوال مساعدة ===

    def calculate_skill_level(self, user):
        """مستوى المهارة من مستوى المستخدم أو من المشاريع المكتملة"""
        if getattr(user, 'is_rated', False) and user.level:
            return user.get_level_display()

        completed = ProjectProgress.objects.filter(user=user, status='completed').count()
        if completed == 0:
            return 'مبتدئ'
        if completed <= 2:
            return 'متوسط'
        if completed <= 5:
            return 'متقدم'
        return 'خبير'

    def get_streak_days(self, user):
        """عدد الأيام المتتالية للنشاط من سجلات التقدم والمهام"""
        dates = set()

        for progress in ProjectProgress.objects.filter(user=user):
            if progress.started_at:
                dates.add(timezone.localtime(progress.started_at).date())
            if progress.completed_at:
                dates.add(timezone.localtime(progress.completed_at).date())

        for submission in TaskSubmission.objects.filter(
            user=user,
            is_completed=True,
            completed_at__isnull=False,
        ):
            dates.add(timezone.localtime(submission.completed_at).date())

        if not dates:
            return 0

        today = timezone.localdate()
        check = today
        if check not in dates:
            check = today - timedelta(days=1)
            if check not in dates:
                return 0

        streak = 0
        while check in dates:
            streak += 1
            check -= timedelta(days=1)
        return streak

    def calculate_completion_rate(self, user):
        """معدل إتمام المشاريع ضمن المسارات المنضم إليها"""
        total = Project.objects.filter(
            course__enrolled_learners=user,
            course__is_active=True,
            course__is_archived=False,
            is_active=True,
        ).count()
        if total == 0:
            return 0
        completed = ProjectProgress.objects.filter(user=user, status='completed').count()
        return int(round((completed / total) * 100))

    def get_average_score(self, user):
        """متوسط تقييم المشاريع المكتملة"""
        grades = list(
            ProjectProgress.objects.filter(
                user=user,
                is_graded=True,
                grade_stars__isnull=False,
            ).values_list('grade_stars', flat=True)
        )
        if not grades:
            return 0
        return round(sum(grades) / len(grades), 1)

class LearnerProgressAPIView(APIView):
    """API لمتابعة تقدم المتعلم"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if not user.is_learner:
            return Response({
                'error': _('غير مصرح')
            }, status=status.HTTP_403_FORBIDDEN)
        
        # بيانات التقدم التفصيلية
        progress_data = {
            'overall': {
                'enrollment_date': user.date_joined.strftime('%Y-%m-%d'),
                'days_active': (timezone.now() - user.date_joined).days,
                'total_projects_enrolled': len(user.get_enrolled_courses_list() or []),
                'total_hours_estimated': len(user.get_enrolled_courses_list() or []) * 20,
            },
            'skill_development': self.get_skill_development(user),
            'timeline': self.get_learning_timeline(user),
            'achievements': self.get_achievements(user),
        }
        
        return Response({
            'message': _('تتبع تقدم المتعلم'),
            'progress_data': progress_data,
        })
    
    def get_skill_development(self, user):
        """تطور المهارات"""
        enrolled_courses = user.get_enrolled_courses_list() or []
        
        skills = {}
        for course in enrolled_courses:
            if 'ويب' in course:
                skills['تطوير الويب'] = skills.get('تطوير الويب', 0) + 20
            if 'بيانات' in course:
                skills['تحليل البيانات'] = skills.get('تحليل البيانات', 0) + 25
            if 'ذكاء' in course:
                skills['الذكاء الاصطناعي'] = skills.get('الذكاء الاصطناعي', 0) + 30
            if 'تطبيق' in course:
                skills['تطوير التطبيقات'] = skills.get('تطوير التطبيقات', 0) + 25
        
        return skills
    
    def get_learning_timeline(self, user):
        """خط زمني للتعلم"""
        timeline = []
        enrolled_courses = user.get_enrolled_courses_list() or []
        
        for i, course in enumerate(enrolled_courses[:10]):
            timeline.append({
                'date': (timezone.now() - timedelta(days=i*30)).strftime('%Y-%m'),
                'event': f'الانضمام إلى مشروع {course}',
                'milestone': 'بداية المشروع' if i == 0 else 'مشروع جديد',
            })
        
        return timeline
    
    def get_achievements(self, user):
        """الإنجازات"""
        enrolled_count = len(user.get_enrolled_courses_list() or [])
        
        achievements = []
        
        if enrolled_count >= 1:
            achievements.append({
                'title': 'المبتدئ المتميز',
                'description': 'إكمال أول مشروع',
                'icon': '🎯',
                'unlocked_at': user.date_joined.strftime('%Y-%m-%d'),
            })
        
        if enrolled_count >= 3:
            achievements.append({
                'title': 'المتعلم النشط',
                'description': 'إكمال 3 مشاريع',
                'icon': '⭐',
                'unlocked_at': (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            })
        
        if enrolled_count >= 5:
            achievements.append({
                'title': 'الخبير الصاعد',
                'description': 'إكمال 5 مشاريع',
                'icon': '🏆',
                'unlocked_at': (timezone.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
            })
        
        return achievements