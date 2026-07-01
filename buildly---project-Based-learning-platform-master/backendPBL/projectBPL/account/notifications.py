from django.utils.translation import gettext_lazy as _

from .models import Notification


def serialize_notification(notification):
    return {
        'id': notification.id,
        'title': notification.title,
        'message': notification.message,
        'type': notification.notification_type,
        'timestamp': notification.created_at.isoformat(),
        'read': notification.is_read,
        'project_id': notification.related_project_id,
    }


def create_notification(*, user, title, message, notification_type, related_project_id=None):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_project_id=related_project_id,
    )


def create_account_created_notification(*, user):
    return create_notification(
        user=user,
        title=_('تم إنشاء حسابك بنجاح'),
        message=_(
            'مرحباً بك في منصة التعلم! تم إنشاء حسابك بنجاح '
            'ويمكنك الآن استكشاف المسارات والمشاريع.'
        ),
        notification_type=Notification.TYPE_ACCOUNT_CREATED,
    )


def create_project_started_notification(*, user, project):
    return create_notification(
        user=user,
        title=_('بدأت مشروعاً جديداً'),
        message=_(
            'لقد بدأت العمل على مشروع «{project_title}». '
            'بالتوفيق في رحلتك التعليمية!'
        ).format(project_title=project.title),
        notification_type=Notification.TYPE_PROJECT_STARTED,
        related_project_id=project.id,
    )


def create_project_submitted_notification(*, user, project):
    return create_notification(
        user=user,
        title=_('تم استلام مشروعك'),
        message=_(
            'تم استلام مشروعك «{project_title}» بنجاح. '
            'سيقوم المشرف بمراجعته وإبلاغك عند اكتمال التقييم.'
        ).format(project_title=project.title),
        notification_type=Notification.TYPE_PROJECT_SUBMITTED,
        related_project_id=project.id,
    )


def create_project_graded_notification(*, user, project):
    return create_notification(
        user=user,
        title=_('تم تقييم مشروعك'),
        message=_(
            'قام المشرف بتقييم مشروعك «{project_title}». '
            'يمكنك الآن مشاهدة التقييم والملاحظات.'
        ).format(project_title=project.title),
        notification_type=Notification.TYPE_PROJECT_GRADED,
        related_project_id=project.id,
    )


def create_password_reset_notification(*, user):
    return create_notification(
        user=user,
        title=_('تمت إعادة تعيين كلمة المرور'),
        message=_(
            'تمت إعادة تعيين كلمة المرور لحسابك بنجاح. '
            'إذا لم تقم بهذا الإجراء، يرجى التواصل مع الدعم فوراً.'
        ),
        notification_type=Notification.TYPE_PASSWORD_RESET,
    )
