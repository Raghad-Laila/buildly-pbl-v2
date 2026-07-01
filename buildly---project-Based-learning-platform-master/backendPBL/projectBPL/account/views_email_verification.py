from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from .email_verification import (
    RESEND_COOLDOWN_SECONDS,
    send_verification_otp,
    verify_email_otp,
)
from .notifications import create_account_created_notification
from .serializers import ProfileSerializer, ResendOTPSerializer, VerifyEmailSerializer


def build_user_response(user, request=None):
    serializer = ProfileSerializer(user, context={'request': request})
    return serializer.data


class VerifyEmailView(APIView):
    """تفعيل الحساب عبر رمز التحقق"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        code = serializer.validated_data['code']

        success, message = verify_email_otp(user, code)
        if not success:
            return Response({
                'success': False,
                'message': message,
            }, status=status.HTTP_400_BAD_REQUEST)

        create_account_created_notification(user=user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'success': True,
            'message': message,
            'user': build_user_response(user, request),
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        })


class ResendOTPView(APIView):
    """إعادة إرسال رمز التحقق (وضع التطوير: إرجاع الرمز في الاستجابة)"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        otp_code, cooldown, delivery_payload = send_verification_otp(user)

        if otp_code is None:
            return Response({
                'success': False,
                'message': _('يرجى الانتظار قبل طلب رمز جديد'),
                'resend_available_in': cooldown,
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        response_data = {
            'success': True,
            'message': _('تم إنشاء رمز تحقق جديد'),
            'resend_available_in': RESEND_COOLDOWN_SECONDS,
            **delivery_payload,
        }

        return Response(response_data)
