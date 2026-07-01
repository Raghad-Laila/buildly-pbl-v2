from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import Notification
from .notifications import serialize_notification


class ListNotificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

        return Response({
            'success': True,
            'notifications': [serialize_notification(item) for item in notifications],
            'unread_count': unread_count,
        })


class UnreadNotificationsCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({
            'success': True,
            'unread_count': unread_count,
        })


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user,
        )

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=['is_read'])

        return Response({
            'success': True,
            'message': _('تم تعليم الإشعار كمقروء'),
            'notification': serialize_notification(notification),
        })


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True)

        return Response({
            'success': True,
            'message': _('تم تحديد جميع الإشعارات كمقروءة'),
            'updated_count': updated_count,
        })


class DeleteNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user,
        )
        was_unread = not notification.is_read
        notification.delete()

        return Response({
            'success': True,
            'message': _('تم حذف الإشعار'),
            'was_unread': was_unread,
        })


class DeleteAllNotificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        deleted_count, _ = Notification.objects.filter(user=request.user).delete()

        return Response({
            'success': True,
            'message': _('تم حذف جميع الإشعارات'),
            'deleted_count': deleted_count,
        })
