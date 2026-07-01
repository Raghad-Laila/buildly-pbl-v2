# account/views_favorites.py
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from courses.models import Course
from projects.models import Project
from .models import UserFavorite


def user_can_access_course(user, course):
    if not course.is_active or course.is_archived:
        return False
    if user.is_admin:
        return True
    return course.is_public


def user_can_access_project(user, project):
    if not project.is_active:
        return False
    return user_can_access_course(user, project.course)


def serialize_favorite_course(course, favorited_at):
    return {
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'level_display': course.get_level_display(),
        'category_display': course.get_category_display(),
        'estimated_duration': course.estimated_duration,
        'projects_count': course.get_actual_projects_count(),
        'enrolled_students_count': course.get_enrolled_students_count(),
        'favorited_at': favorited_at,
    }


def serialize_favorite_project(project, favorited_at):
    return {
        'project_id': project.id,
        'course_id': project.course_id,
        'course_title': project.course.title,
        'title': project.title,
        'description': project.description,
        'level_display': project.get_level_display(),
        'language_display': project.get_language_display(),
        'estimated_time': project.estimated_time,
        'favorited_at': favorited_at,
    }


class ListFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = UserFavorite.objects.filter(user=request.user).order_by('-created_at')

        course_map = {}
        project_map = {}
        for favorite in favorites:
            if favorite.item_type == UserFavorite.ITEM_TYPE_COURSE:
                course_map[favorite.object_id] = favorite.created_at
            elif favorite.item_type == UserFavorite.ITEM_TYPE_PROJECT:
                project_map[favorite.object_id] = favorite.created_at

        favorite_courses = []
        if course_map:
            courses = Course.objects.filter(id__in=course_map.keys())
            for course in courses:
                if user_can_access_course(request.user, course):
                    favorite_courses.append(
                        serialize_favorite_course(course, course_map[course.id])
                    )

        favorite_projects = []
        if project_map:
            projects = Project.objects.select_related('course').filter(id__in=project_map.keys())
            for project in projects:
                if user_can_access_project(request.user, project):
                    favorite_projects.append(
                        serialize_favorite_project(project, project_map[project.id])
                    )

        favorite_courses.sort(key=lambda item: item['favorited_at'], reverse=True)
        favorite_projects.sort(key=lambda item: item['favorited_at'], reverse=True)

        return Response({
            'success': True,
            'message': _('تم جلب المفضلة بنجاح'),
            'favorite_course_ids': [course['id'] for course in favorite_courses],
            'favorite_project_ids': [project['project_id'] for project in favorite_projects],
            'courses': favorite_courses,
            'projects': favorite_projects,
            'count': len(favorite_courses) + len(favorite_projects),
        })


class ToggleFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item_type = request.data.get('item_type')
        object_id = request.data.get('object_id')

        if item_type not in (UserFavorite.ITEM_TYPE_COURSE, UserFavorite.ITEM_TYPE_PROJECT):
            return Response({
                'success': False,
                'message': _('نوع العنصر غير صالح'),
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            object_id = int(object_id)
        except (TypeError, ValueError):
            return Response({
                'success': False,
                'message': _('معرف العنصر غير صالح'),
            }, status=status.HTTP_400_BAD_REQUEST)

        if item_type == UserFavorite.ITEM_TYPE_COURSE:
            try:
                course = Course.objects.get(id=object_id)
            except Course.DoesNotExist:
                return Response({
                    'success': False,
                    'message': _('المسار غير موجود'),
                }, status=status.HTTP_404_NOT_FOUND)

            if not user_can_access_course(request.user, course):
                return Response({
                    'success': False,
                    'message': _('لا يمكنك إضافة هذا المسار للمفضلة'),
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                project = Project.objects.select_related('course').get(id=object_id)
            except Project.DoesNotExist:
                return Response({
                    'success': False,
                    'message': _('المشروع غير موجود'),
                }, status=status.HTTP_404_NOT_FOUND)

            if not user_can_access_project(request.user, project):
                return Response({
                    'success': False,
                    'message': _('لا يمكنك إضافة هذا المشروع للمفضلة'),
                }, status=status.HTTP_403_FORBIDDEN)

        favorite = UserFavorite.objects.filter(
            user=request.user,
            item_type=item_type,
            object_id=object_id,
        ).first()

        if favorite:
            favorite.delete()
            return Response({
                'success': True,
                'message': _('تمت إزالة العنصر من المفضلة'),
                'is_favorite': False,
                'item_type': item_type,
                'object_id': object_id,
            })

        UserFavorite.objects.create(
            user=request.user,
            item_type=item_type,
            object_id=object_id,
        )

        return Response({
            'success': True,
            'message': _('تمت إضافة العنصر إلى المفضلة'),
            'is_favorite': True,
            'item_type': item_type,
            'object_id': object_id,
        }, status=status.HTTP_201_CREATED)
