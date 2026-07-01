from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from .notifications import create_password_reset_notification
from .password_reset import (
    GENERIC_REQUEST_MESSAGE,
    RESEND_COOLDOWN_SECONDS,
    request_password_reset,
    reset_password_with_token,
    verify_password_reset_otp,
)
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifyOTPSerializer,
)


class PasswordResetRequestView(APIView):
    """طلب إعادة تعيين كلمة المرور عبر البريد الإلكتروني"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        result = request_password_reset(email)

        if result.get('cooldown_active'):
            return Response({
                'success': False,
                'message': _('يرجى الانتظار قبل طلب رمز جديد'),
                'resend_available_in': result['resend_available_in'],
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response({
            'success': True,
            'message': GENERIC_REQUEST_MESSAGE,
            'resend_available_in': result['resend_available_in'],
            **result['delivery_payload'],
        })


class PasswordResetResendOTPView(APIView):
    """إعادة إنشاء رمز تحقق لإعادة تعيين كلمة المرور"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        result = request_password_reset(email)

        if not result.get('user_found'):
            return Response({
                'success': True,
                'message': GENERIC_REQUEST_MESSAGE,
                'resend_available_in': RESEND_COOLDOWN_SECONDS,
            })

        if result.get('cooldown_active'):
            return Response({
                'success': False,
                'message': _('يرجى الانتظار قبل طلب رمز جديد'),
                'resend_available_in': result['resend_available_in'],
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response({
            'success': True,
            'message': _('تم إنشاء رمز تحقق جديد'),
            'resend_available_in': result['resend_available_in'],
            **result['delivery_payload'],
        })


class PasswordResetVerifyOTPView(APIView):
    """التحقق من رمز OTP قبل إعادة تعيين كلمة المرور"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        code = serializer.validated_data['code']

        success, message, reset_token = verify_password_reset_otp(user, code)
        if not success:
            return Response({
                'success': False,
                'message': message,
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'message': message,
            'reset_token': reset_token,
        })


class PasswordResetConfirmView(APIView):
    """تعيين كلمة مرور جديدة بعد التحقق من OTP"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, message, user = reset_password_with_token(
            serializer.validated_data['reset_token'],
            serializer.validated_data['new_password'],
        )

        if not success:
            return Response({
                'success': False,
                'message': message,
            }, status=status.HTTP_400_BAD_REQUEST)

        create_password_reset_notification(user=user)

        return Response({
            'success': True,
            'message': message,
        })
