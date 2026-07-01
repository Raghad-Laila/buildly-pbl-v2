# courses/urls.py
from django.urls import path
from .views import (
    CreateCourseView, 
    ListCoursesView,
    UpdateCourseView,
    RetrieveCourseView,
    DeleteCourseView,      
    ConfirmDeleteCourseView,
    ConfirmArchiveCourseView,
    ArchiveCourseView,
    ListArchivedCoursesView,
    CourseDetailView,
    JoinCourseView,
    UserEnrolledCoursesView,
    CheckEnrollmentView
)

app_name = 'courses'

urlpatterns = [
    path('', ListCoursesView.as_view(), name='list-courses'),
    path('create/', CreateCourseView.as_view(), name='create-course'),
    path('my-courses/', UserEnrolledCoursesView.as_view(), name='my-courses'),
    path('archived/', ListArchivedCoursesView.as_view(), name='list-archived-courses'),
    path('<int:id>/update/', UpdateCourseView.as_view(), name='update-course'),
    path('<int:id>/confirm-delete/', ConfirmDeleteCourseView.as_view(), name='confirm-delete'),
    path('<int:id>/confirm-archive/', ConfirmArchiveCourseView.as_view(), name='confirm-archive'),
    path('<int:id>/archive/', ArchiveCourseView.as_view(), name='archive-course'),
    path('<int:id>/delete/', DeleteCourseView.as_view(), name='delete-course'),
    path('<int:id>/details/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:id>/join/', JoinCourseView.as_view(), name='join-course'),
    path('<int:id>/check-enrollment/', CheckEnrollmentView.as_view(), name='check-enrollment'),
    path('<int:id>/', RetrieveCourseView.as_view(), name='retrieve-course'),
]