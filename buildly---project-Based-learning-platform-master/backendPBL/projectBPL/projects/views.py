# projects/views.py
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Project, ProjectStarterFile, ProjectTask, TaskSubmission, Tests, WorkspaceBranch
from .serializers import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectTaskSerializer,
    ProjectUpdateSerializer,
    ProjectDeleteConfirmationSerializer,
    ProjectStarterFileSerializer,
    TaskSubmissionSerializer,
    TestsSerializer,
    WorkspaceBranchListSerializer,
    WorkspaceBranchDetailSerializer,
    WorkspaceBranchCreateSerializer,
    WorkspaceBranchUpdateSerializer,
)
from courses.models import Course
from progress.models import ProjectProgress
from account.notifications import create_project_started_notification
from rest_framework.parsers import MultiPartParser, FormParser
from reversion.views import RevisionMixin
import reversion
from reversion.models import Version
from .test_runner import run_python_in_docker, run_project_tests
from .starter_utils import build_starter_zip_from_uploads
from .ai_review import AIReviewService
from .ai_review.schemas import AIReviewRequestSchema
from .code_quality import CodeQualityReviewService
from .code_quality.schemas import CodeQualityRequestSchema
from .workspace_branch_utils import ensure_main_branch
import subprocess
from django.db import IntegrityError


def get_learner_projects_queryset(user):
    """مشاريع المسارات التي انضم إليها المتعلم فقط."""
    return Project.objects.filter(
        course__enrolled_learners=user,
        course__is_active=True,
        course__is_archived=False,
        is_active=True,
    )


def learner_can_access_course(user, course):
    if user.is_admin:
        return True
    return course.is_student_enrolled(user)


class IsCourseInstructor(permissions.BasePermission):
    """التحقق من أن المستخدم هو مشرف (أي مشرف في النظام)"""
    
    def has_permission(self, request, view):
        # السماح للجميع بالوصول للقراءة فقط
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # لإنشاء/تعديل مشروع، يجب أن يكون المستخدم مشرفاً (أي مشرف في النظام)
        if not request.user.is_admin:
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """أي مشرف يستطيع تعديل أي مشروع"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # فقط المشرفين يمكنهم التعديل
        if not request.user.is_admin:
            return False
        
        return True


class CreateProjectView(RevisionMixin, generics.CreateAPIView):
    """واجهة إنشاء مشروع جديد"""
    
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # حفظ المشروع
            project = serializer.save()
            
            return Response({
                'success': True,
                'message': _('تم إنشاء المشروع بنجاح'),
                'project': {
                    'project_id': project.id,  # ⭐ تغيير: استخدام id
                    'course_id': project.course.id,  # ⭐ تغيير: استخدام course.id بدلاً من path_id
                    'title': project.title,
                    'description': project.description,
                    'estimated_time': project.estimated_time,
                    'level': project.get_level_display(),
                    'language': project.get_language_display(),
                    'image': project.image.url if project.image else None,
                    'created_at': project.created_at,
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            error_messages = []
            
            if hasattr(e, 'detail'):
                if isinstance(e.detail, dict):
                    for field, errors in e.detail.items():
                        if isinstance(errors, list):
                            for error in errors:
                                error_messages.append(f"{field}: {error}")
                        else:
                            error_messages.append(f"{field}: {errors}")
                else:
                    error_messages.append(str(e.detail))
            else:
                error_messages.append(str(e))
            
            # رسالة مبسطة للمستخدم
            user_message = _('فشل إنشاء المشروع')
            if any('يوجد بالفعل مشروع بهذا العنوان' in msg for msg in error_messages):
                user_message = _('يوجد مشروع بنفس العنوان في هذا المسار. الرجاء استخدام عنوان مختلف.')
            
            return Response({
                'success': False,
                'message': user_message,
                'errors': error_messages,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # التحقق من خطأ القيد الفريد
            error_message = str(e)
            user_message = _('حدث خطأ أثناء إنشاء المشروع')
            
            if 'unique_project_title_per_course' in error_message or 'UNIQUE constraint failed' in error_message:
                user_message = _('يوجد مشروع بنفس العنوان في هذا المسار. الرجاء استخدام عنوان مختلف.')
            
            return Response({
                'success': False,
                'message': user_message,
                'error': error_message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListProjectsView(generics.ListAPIView):
    """واجهة عرض قائمة المشاريع"""
    
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def apply_search_filter(self, queryset):
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return queryset

        return queryset.filter(title__icontains=search)

    def get_queryset(self):
        user = self.request.user
        
        # فلترة حسب المسار إذا تم تمرير course_id
        course_id = self.request.query_params.get('course_id', None)
        
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                
                if user.is_admin:
                    queryset = Project.objects.filter(course=course, is_active=True)
                elif learner_can_access_course(user, course):
                    queryset = Project.objects.filter(course=course, is_active=True)
                else:
                    return Project.objects.none()

                return self.apply_search_filter(queryset)
                        
            except Course.DoesNotExist:
                return Project.objects.none()
        
        # بدون فلترة
        if user.is_admin:
            queryset = Project.objects.filter(is_active=True).order_by('course', 'order')
        else:
            queryset = get_learner_projects_queryset(user).order_by('course', 'order')

        return self.apply_search_filter(queryset)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            search = request.query_params.get('search', '').strip()
            if search:
                message = _('لا توجد مشاريع مطابقة لبحثك')
            elif not request.user.is_admin:
                message = _('لا توجد مشاريع في مساراتك المنضم إليها')
            else:
                message = _('لا توجد مشاريع متاحة')
            return Response({
                'message': message,
                'projects': [],
                'count': 0,
                'search': search,
            })
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': _('تم جلب المشاريع بنجاح'),
            'count': queryset.count(),
            'search': request.query_params.get('search', '').strip(),
            'projects': serializer.data
        })


class ProjectDetailView(generics.RetrieveAPIView):
    """واجهة عرض تفاصيل مشروع معين (UC-05 الخطوة 3)"""
    
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'  # ⭐ تغيير: استخدام pk بدلاً من project_id
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return Project.objects.filter(is_active=True)
        return get_learner_projects_queryset(user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        
        return Response({
            'success': True,
            'message': _('تم جلب تفاصيل المشروع بنجاح'),
            'project': serializer.data,
            # 'available_levels': dict(Project.LEVEL_CHOICES),
            # 'available_languages': dict(Project.PROGRAMMING_LANGUAGE_CHOICES),
            # 'can_edit': request.user.is_admin
        })


class CourseProjectsView(generics.ListAPIView):
    """واجهة عرض مشاريع مسار معين"""
    
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # ⭐ تغيير: استخدام course_id بدلاً من path_id
        course_id = self.kwargs.get('course_id')
        
        try:
            # ⭐ تغيير: البحث باستخدام id بدلاً من pathid
            self.course = Course.objects.get(id=course_id)
            
            if user.is_admin:
                return Project.objects.filter(course=self.course, is_active=True)
            if learner_can_access_course(user, self.course):
                return Project.objects.filter(course=self.course, is_active=True)
            
            return Project.objects.none()
            
        except Course.DoesNotExist:
            raise ValidationError(_('المسار التعليمي غير موجود'))
    
    def list(self, request, *args, **kwargs):
        """تعديل الـ response لإضافة معلومات إضافية"""
        try:
            queryset = self.get_queryset()
            
            if not queryset.exists():
                return Response({
                    'message': _('لا توجد مشاريع في هذا المسار'),
                    'projects': [],
                    'course_info': {
                        'course_id': self.course.id,  # ⭐ تغيير
                        'title': self.course.title,
                        'total_projects_in_course': self.course.projects_count,
                        'has_projects': False
                    }
                })
            
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'message': _('تم جلب مشاريع المسار بنجاح'),
                'count': queryset.count(),
                'course_info': {
                    'course_id': self.course.id,  # ⭐ تغيير
                    'title': self.course.title,
                    'instructor': f"{self.course.instructor.first_name} {self.course.instructor.last_name}",
                    'total_projects_in_course': self.course.projects_count,
                    'is_public': self.course.is_public,
                    'is_active': self.course.is_active
                },
                'projects': serializer.data
            })
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _('خطأ في جلب المشاريع'),
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class UpdateProjectView(RevisionMixin, generics.UpdateAPIView):
    """واجهة تعديل مشروع موجود (UC-05)"""
    
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'pk'
    
    def get_object(self):
        """الحصول على المشروع المطلوب"""
        pk = self.kwargs.get('pk')
        try:
            return Project.objects.get(id=pk, is_active=True)
        except Project.DoesNotExist:
            raise ValidationError(_('المشروع المطلوب غير موجود'))
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """تحديث بيانات المشروع"""
        kwargs['partial'] = True  # اجعلها partial دائماً لتجنب مشاكل الحقول المفقودة في FormData
        return self.update_project(request, *args, **kwargs)

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        """تحديث جزئي للمشروع"""
        kwargs['partial'] = True
        return self.update_project(request, *args, **kwargs)

    def update_project(self, request, *args, **kwargs):
        try:
            partial = kwargs.get('partial', False)
            project = self.get_object()
            
            serializer = self.get_serializer(
                project,
                data=request.data,
                partial=partial,
                context={'instance': project, 'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            updated_project = serializer.save()
            
            return Response({
                'success': True,
                'message': _('تم تعديل المشروع بنجاح'),
                'project': {
                    'project_id': updated_project.id,
                    'course_id': updated_project.course.id,
                    'title': updated_project.title,
                    'description': updated_project.description,
                    'requirements': updated_project.requirements,
                    'objectives': updated_project.objectives,
                    'estimated_time': updated_project.estimated_time,
                    'level': updated_project.get_level_display(),
                    'language': updated_project.get_language_display(),
                    'image': updated_project.image.url if updated_project.image else None,
                    'order': updated_project.order,
                    'updated_by': f"{request.user.first_name} {request.user.last_name}",
                    'updated_at': updated_project.updated_at,
                }
            })
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _('فشل تعديل المشروع'),
                'errors': e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': _('حدث خطأ أثناء تعديل المشروع'),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



# projects/views.py - إضافة View للحذف
# projects/views.py - تحديث DeleteProjectView ليكون حذف فعلي بعد التأكيد

class DeleteProjectView(generics.DestroyAPIView):
    """واجهة حذف مشروع فعلي بعد التأكيد (UC-06 الخطوة 6-7)"""
    
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'pk'
    
    def get_object(self):
        """الحصول على المشروع المطلوب للحذف"""
        pk = self.kwargs.get('pk')
        try:
            return Project.objects.get(id=pk, is_active=True)
        except Project.DoesNotExist:
            raise ValidationError(_('المشروع المطلوب غير موجود'))
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        UC-06 الخطوة 6-7: حذف المشروع فعلياً
        """
        try:
            # الحصول على المشروع
            project = self.get_object()
            
            # حفظ معلومات المشروع قبل الحذف
            project_info = {
                'project_id': project.id,
                'title': project.title,
                'course_id': project.course.id,
                'course_title': project.course.title,
                'level': project.get_level_display(),
                'language': project.get_language_display(),
                'estimated_time': project.estimated_time,
                'created_at': project.created_at,
            }
            
            # الحذف الفعلي (استخدام delete() بدلاً من soft_delete())
            project.delete()
            
            # الخطوة 7: عرض رسالة نجاح
            return Response({
                'success': True,
                'message': _('✅ تم حذف المشروع بنجاح'),
                'deleted_project': project_info,
                'deletion_details': {
                    'deleted_by': f"{request.user.first_name} {request.user.last_name}",
                    'deleted_at': timezone.now(),
                    'course_remaining_projects': Project.objects.filter(
                        course_id=project_info['course_id'],
                        is_active=True
                    ).count(),
                    'action': _('المشروع تم حذفه بشكل دائم من النظام')
                },
                'redirect_info': {
                    'redirect_url': f"/courses/{project_info['course_id']}/projects",
                    'message': _('سيتم إعادة توجيهك إلى صفحة مشاريع المسار')
                }
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _('❌ فشل حذف المشروع'),
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': _('❌ حدث خطأ أثناء حذف المشروع'),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ConfirmDeleteProjectView(generics.RetrieveAPIView):
    """واجهة تأكيد حذف مشروع (UC-06 الخطوة 4)"""
    
    serializer_class = ProjectDeleteConfirmationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Project.objects.filter(is_active=True)
    
    def get_object(self):
        """الحصول على المشروع المطلوب"""
        pk = self.kwargs.get('pk')
        try:
            return Project.objects.get(id=pk, is_active=True)
        except Project.DoesNotExist:
            raise ValidationError(_('المشروع المطلوب غير موجود'))
    
    def retrieve(self, request, *args, **kwargs):
        """
        UC-06 الخطوة 4: عرض نافذة تأكيد الحذف
        """
        try:
            project = self.get_object()
            serializer = self.get_serializer(project)
            
            response_data = {
                'success': True,
                'message': _('⚠️ تأكيد حذف المشروع'),
                'confirmation_required': True,
                'project': serializer.data,
                'confirmation_details': {
                    'title': _('هل أنت متأكد من حذف هذا المشروع؟'),
                    'warning': _('هذا الإجراء لا يمكن التراجع عنه'),
                    'consequences': [
                        _('المشروع سيحذف من النظام بشكل دائم'),
                        _('جميع البيانات المرتبطة بالمشروع ستُحذف'),
                        _('لا يمكن استعادة المشروع بعد الحذف')
                    ],
                    'action_buttons': [
                        {
                            'label': _('نعم، احذف المشروع'),
                            'action': 'confirm_delete',
                            'url': f'/api/projects/{project.id}/delete/',
                            'method': 'DELETE',
                            'style': 'danger'
                        },
                        {
                            'label': _('إلغاء'),
                            'action': 'cancel',
                            'style': 'secondary'
                        }
                    ]
                }
            }
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _('المشروع غير موجود'),
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class StartProjectView(APIView):
    """واجهة بدء المشروع من قبل المتعلم (بدون نموذج تقدم)"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """
        بدء مشروع معين من قبل المتعلم
        """
        try:
            # 1. التحقق من وجود المشروع
            try:
                project = Project.objects.get(id=pk, is_active=True)
            except Project.DoesNotExist:
                return Response({
                    'success': False,
                    'message': _('المشروع غير موجود')
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 2. التحقق من أن المستخدم متعلم
            if not request.user.is_learner:
                return Response({
                    'success': False,
                    'message': _('فقط المتعلمين يمكنهم بدء المشاريع')
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 3. التحقق من أن الطالب منضم للمسار
            if not project.course.is_student_enrolled(request.user):
                return Response({
                    'success': False,
                    'message': _('يجب الانضمام للمسار أولاً لبدء المشروع')
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            progress, created = ProjectProgress.objects.get_or_create(
                user=request.user,
                project=project
            )

            if progress.status == 'completed':
                return Response({
                    'success': False,
                    'message': _('لا يمكنك بدء هذا المشروع لأنه مكتمل بالفعل'),
                    'status': 'completed'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            previous_projects = Project.objects.filter(
                course=project.course,
                order__lt=project.order,
                is_active=True
            )

            incomplete_previous = ProjectProgress.objects.filter(
                user=request.user,
                project__in=previous_projects
            ).exclude(status='completed').select_related('project').order_by('project__order').first()

            if not incomplete_previous:
                started_project_ids = ProjectProgress.objects.filter(
                    user=request.user,
                    project__in=previous_projects
                ).values_list('project_id', flat=True)

                not_started_projects = previous_projects.exclude(id__in=started_project_ids).order_by('order').first()

                if not_started_projects:
                    return Response({
                        'success': False,
                        'message': _('يجب إكمال المشاريع السابقة أولاً'),
                        'required_project': {
                            'id': not_started_projects.id,
                            'title': not_started_projects.title,
                            'order': not_started_projects.order,
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    'success': False,
                    'message': _('يجب إكمال المشاريع السابقة أولاً'),
                    'required_project': {
                        'id': incomplete_previous.project.id,
                        'title': incomplete_previous.project.title,
                        'order': incomplete_previous.project.order,
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            if progress.status == 'not_started':
                progress.status = 'in_progress'
                progress.started_at = timezone.now()
                progress.progress_percentage = 0
                progress.save()

                create_project_started_notification(user=request.user, project=project)

            elif progress.status == 'in_progress':
                return Response({
                    'success': True,
                    'message': _('المشروع قيد التنفيذ بالفعل'),
                }, status=status.HTTP_200_OK)

            elif progress.status == 'completed':
                return Response({
                    'success': True,
                    'message': _('لقد أكملت هذا المشروع بالفعل'),
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': True,
                'message': _('🎉 تم بدء المشروع بنجاح!'),
                'project': {
                    'id': project.id,
                    'title': project.title,
                    'description': project.description[:100] + '...',
                    'estimated_time': project.estimated_time,
                    'level': project.get_level_display(),
                    'language': project.get_language_display()
                },
                'instructions': _('يمكنك الآن البدء في تنفيذ المشروع'),
                'next_steps': [
                    _('1. اقرأ المتطلبات والأهداف'),
                    _('2. جهز البيئة اللازمة'),
                    _('3. ابدأ بتنفيذ الخطوات'),
                    _('4. اطلب المساعدة إذا احتجت')
                ]
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': _('حدث خطأ أثناء بدء المشروع'),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UploadStarterFileView(RevisionMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk, is_active=True)

            uploaded_files = request.FILES.getlist('files')
            single_file = request.FILES.get('file')

            if uploaded_files:
                zip_name = f'project_{project.id}_starter.zip'
                try:
                    zip_file = build_starter_zip_from_uploads(uploaded_files, zip_name=zip_name)
                except ValueError as exc:
                    return Response({
                        'success': False,
                        'message': str(exc),
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif single_file:
                zip_file = single_file
            else:
                return Response({
                    'success': False,
                    'message': _('لم يتم إرسال أي مجلد')
                }, status=status.HTTP_400_BAD_REQUEST)

            starter, created = ProjectStarterFile.objects.update_or_create(
                project=project,
                defaults={
                    'file': zip_file,
                    'uploaded_by': request.user
                }
            )

            return Response({
                'success': True,
                'message': _('تم رفع مجلد البداية بنجاح'),
                'file': {
                    'url': starter.file.url,
                    'file_name': starter.file.name.split('/')[-1],
                    'uploaded_at': starter.uploaded_at
                }
            })

        except Project.DoesNotExist:
            return Response({
                'success': False,
                'message': _('المشروع غير موجود')
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': _('حدث خطأ أثناء رفع مجلد البداية'),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProjectTaskView(RevisionMixin, generics.CreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError(_('المشروع غير موجود'))

        serializer.save(project=project)
        
class ProjectTasksListView(generics.ListAPIView):
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')

        return ProjectTask.objects.filter(
            project_id=project_id
        ).order_by('order')
    

class ProjectTaskDeleteView(RevisionMixin, generics.DestroyAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'id'


class CreateTestsView(RevisionMixin, generics.CreateAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError(_('المشروع غير موجود'))

        serializer.save(project=project)


class ProjectTestsListView(generics.ListAPIView):
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Tests.objects.filter(project_id=project_id).order_by('id')


class ProjectTestDetailView(generics.RetrieveAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class UpdateTestsView(RevisionMixin, generics.UpdateAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'id'


class ProjectTestDeleteView(RevisionMixin, generics.DestroyAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]
    lookup_field = 'id'


class RunProjectTestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        code = request.data.get('code')
        language = request.data.get('language', 'python')

        if not code or not str(code).strip():
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'المشروع غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        tests = Tests.objects.filter(project=project).order_by('id')

        if not tests.exists():
            return Response(
                {
                    'success': True,
                    'results': [],
                    'summary': {'total': 0, 'passed': 0, 'failed': 0},
                }
            )

        payload = run_project_tests(code, language or project.get_languages_list()[0] or project.language, tests)

        return Response(
            {
                'success': True,
                **payload,
            }
        )
        

class ExecuteCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        language = request.data.get("language", "python")
        files = request.data.get("files")
        entry_file_name = (
            request.data.get("entryFileName")
            or request.data.get("entry_file_name")
            or "main.py"
        )

        has_files = isinstance(files, list) and len(files) > 0

        if not has_files and not code:
            return Response({"error": "No code provided"}, status=400)

        frontend_languages = {'html', 'css', 'javascript', 'typescript', 'react'}
        if language in frontend_languages:
            return Response({
                "error": "لغات الفرونت إند تُنفَّذ من المتصفح مباشرة. حدّث الصفحة وحاول مرة أخرى."
            }, status=400)

        if language != "python":
            return Response({
                "error": f"تنفيذ لغة '{language}' غير مدعوم على السيرفر حالياً. يدعم السيرفر Python فقط."
            }, status=400)

        try:
            if has_files:
                outcome = run_python_in_docker(
                    files=files,
                    entry_file_name=entry_file_name,
                )
            else:
                outcome = run_python_in_docker(code)

            return Response({
                "stdout": outcome["stdout"],
                "stderr": outcome["stderr"],
                "returncode": outcome["returncode"],
            })

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=400)

        except subprocess.TimeoutExpired:
            return Response({
                "error": "Execution timeout"
            }, status=400)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)


class AIReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AIReviewRequestSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.validated_data['project_id']
        files = serializer.validated_data['files']
        test_summary = serializer.validated_data.get('test_summary')
        failed_tests = serializer.validated_data.get('failed_tests')
        test_error = serializer.validated_data.get('test_error')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'المشروع غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        result = AIReviewService().review(
            project=project,
            files=files,
            test_summary=test_summary,
            failed_tests=failed_tests,
            test_error=test_error,
        )
        return Response(result)


class CodeQualityReviewView(APIView):
    """Post-success code quality review (FR-2). Separate from AI Assistant (FR-1)."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CodeQualityRequestSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.validated_data['project_id']
        files = serializer.validated_data['files']
        test_summary = serializer.validated_data.get('test_summary')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'المشروع غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        result = CodeQualityReviewService().review(
            project=project,
            files=files,
            test_summary=test_summary,
        )
        return Response(result)


class SaveTaskSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        try:
            task = ProjectTask.objects.get(id=task_id)

            progress, created = TaskSubmission.objects.get_or_create(
                user=request.user,
                task=task,
                defaults={'project': task.project}
            )

            answer = request.data.get('answer', '')
            status = request.data.get('status', 'in_progress')

            progress.answer = answer
            progress.status = status

            # Completion Logic
            if status == 'completed':
                progress.is_completed = True
                progress.completed_at = timezone.now()
            else:
                progress.is_completed = False
                progress.completed_at = None

            progress.save()

            return Response({
                'success': True,
                'message': _('تم حفظ التقدم بنجاح'),
                'progress': {
                    'task_id': task.id,
                    'status': progress.status,
                    'is_completed': progress.is_completed,
                    'last_saved_at': progress.last_saved_at,
                    'completed_at': progress.completed_at,
                }
            })

        except ProjectTask.DoesNotExist:
            return Response({
                'success': False,
                'message': _('المهمة غير موجودة')
            }, status=404)

        except Exception as e:
            return Response({
                'success': False,
                'message': _('خطأ أثناء الحفظ'),
                'error': str(e)
            }, status=500)
            
            
class GetTaskSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        try:
            progress = TaskSubmission.objects.get(
                user=request.user,
                task_id=task_id
            )

            return Response({
                'success': True,
                'progress': TaskSubmissionSerializer(progress).data
            })

        except TaskSubmission.DoesNotExist:
            return Response({
                'success': True,
                'progress': None
            })
        

class AdminTaskFeedbackView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def post(self, request, task_id):
        user_id = request.data.get('userId')
        admin_feedback = request.data.get('feedback')
        is_correct = request.data.get('is_correct', True)

        if not user_id:
            return Response({'error': 'userId is required'}, status=status.HTTP_400_BAD_REQUEST)

        submission = get_object_or_404(TaskSubmission, task_id=task_id, user_id=user_id)

        submission.admin_feedback = admin_feedback
        submission.is_correct = is_correct
        submission.reviewed_at = timezone.now()
        submission.save()

        return Response({
            'message': 'Task feedback saved successfully',
            'task_id': task_id,
            'user_id': user_id
        })
    
class AdminGetStudentSubmissionView(APIView):
   
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]

    def get(self, request, task_id, user_id):
        
        submission = get_object_or_404(TaskSubmission, task_id=task_id, user_id=user_id)
        
        return Response({
            'id': submission.id,
            'answer': submission.answer,
            'admin_feedback': submission.admin_feedback,
            'is_correct': submission.is_correct,
            'status': submission.status,
            'is_completed': submission.is_completed,
            'last_saved_at': submission.last_saved_at,
            'reviewed_at': submission.reviewed_at
        })

class ProjectVersionHistoryView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        versions = Version.objects.get_for_object(project)
        
        data = [{
            'version_id': v.id,
            'date': v.revision.date_created,
            'user': v.revision.user.email if v.revision.user else "System",
            'comment': v.revision.comment
        } for v in versions]
        
        return Response(data)

class ProjectRollbackView(APIView):
    def get(self, request, project_id, version_id):
        version = get_object_or_404(Version, id=version_id)
        version.revision.revert() 
        return Response({"message": "تم استعادة النسخة بنجاح"})


class WorkspaceBranchListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        ensure_main_branch(request.user, project)

        branches = WorkspaceBranch.objects.filter(
            user=request.user,
            project=project,
        ).order_by('-is_main', 'name')

        serializer = WorkspaceBranchListSerializer(branches, many=True)
        return Response({
            'success': True,
            'branches': serializer.data,
            'count': len(serializer.data),
        })

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        main_branch = ensure_main_branch(request.user, project)

        serializer = WorkspaceBranchCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']

        if WorkspaceBranch.objects.filter(
            user=request.user,
            project=project,
            name=name,
        ).exists():
            return Response(
                {
                    'success': False,
                    'message': _('A branch with this name already exists.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            branch = WorkspaceBranch.objects.create(
                user=request.user,
                project=project,
                name=name,
                files_json=main_branch.files_json,
                is_main=False,
            )
        except IntegrityError:
            return Response(
                {
                    'success': False,
                    'message': _('A branch with this name already exists.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'success': True,
                'branch': WorkspaceBranchDetailSerializer(branch).data,
            },
            status=status.HTTP_201_CREATED,
        )


class WorkspaceBranchDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _get_owned_branch(self, request, branch_id):
        branch = get_object_or_404(WorkspaceBranch, id=branch_id)
        if branch.user_id != request.user.id:
            raise PermissionDenied(_('You do not have access to this branch.'))
        return branch

    def get(self, request, branch_id):
        branch = self._get_owned_branch(request, branch_id)
        return Response({
            'success': True,
            'branch': WorkspaceBranchDetailSerializer(branch).data,
        })

    def patch(self, request, branch_id):
        branch = self._get_owned_branch(request, branch_id)
        serializer = WorkspaceBranchUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if 'name' in data:
            name = data['name']
            conflict = WorkspaceBranch.objects.filter(
                user=request.user,
                project=branch.project,
                name=name,
            ).exclude(id=branch.id)
            if conflict.exists():
                return Response(
                    {
                        'success': False,
                        'message': _('A branch with this name already exists.'),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            branch.name = name

        if 'files_json' in data:
            branch.files_json = data['files_json']

        try:
            branch.save()
        except IntegrityError:
            return Response(
                {
                    'success': False,
                    'message': _('A branch with this name already exists.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'success': True,
            'branch': WorkspaceBranchDetailSerializer(branch).data,
        })

    def delete(self, request, branch_id):
        branch = self._get_owned_branch(request, branch_id)

        if branch.is_main:
            return Response(
                {
                    'success': False,
                    'message': _('The Main branch cannot be deleted.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        branch.delete()
        return Response({
            'success': True,
            'message': _('Branch deleted successfully.'),
        })


class WorkspaceBranchMergeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, branch_id):
        source_branch = get_object_or_404(WorkspaceBranch, id=branch_id)

        if source_branch.user_id != request.user.id:
            raise PermissionDenied(_('You do not have access to this branch.'))

        if source_branch.is_main:
            return Response(
                {
                    'message': _('Main branch cannot be merged into itself.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        main_branch = WorkspaceBranch.objects.filter(
            user=request.user,
            project=source_branch.project,
            is_main=True,
        ).first()

        if not main_branch:
            return Response(
                {
                    'message': _('Main branch was not found for this project.'),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            main_branch.files_json = source_branch.files_json
            main_branch.save(update_fields=['files_json', 'updated_at'])

            code_task_ids = ProjectTask.objects.filter(
                project=source_branch.project,
                task_type='code',
            ).values_list('id', flat=True)

            TaskSubmission.objects.filter(
                user=request.user,
                project=source_branch.project,
                task_id__in=code_task_ids,
            ).update(answer=source_branch.files_json)

        return Response({
            'message': 'Branch merged successfully.',
        })
