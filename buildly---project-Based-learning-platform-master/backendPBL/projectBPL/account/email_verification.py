from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import EmailVerificationOTP
from .otp_delivery import deliver_otp
from .otp_utils import generate_otp_code, hash_value, verify_hash

OTP_EXPIRY_MINUTES = 10
RESEND_COOLDOWN_SECONDS = 60


def get_resend_cooldown_remaining(user):
    latest_otp = (
        EmailVerificationOTP.objects
        .filter(user=user)
        .order_by('-created_at')
        .first()
    )
    if not latest_otp:
        return 0

    elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
    remaining = RESEND_COOLDOWN_SECONDS - elapsed
    return max(0, int(remaining))


def create_verification_otp(user):
    """إنشاء رمز تحقق جديد وإبطال الرموز السابقة غير المستخدمة"""
    EmailVerificationOTP.objects.filter(
        user=user,
        is_used=False,
    ).update(is_used=True)

    code = generate_otp_code()
    expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    EmailVerificationOTP.objects.create(
        user=user,
        code_hash=hash_value(code),
        expires_at=expires_at,
    )

    return code


def verify_email_otp(user, code):
    otp = (
        EmailVerificationOTP.objects
        .filter(user=user, is_used=False)
        .order_by('-created_at')
        .first()
    )

    if not otp:
        return False, _('لا يوجد رمز تحقق صالح. يرجى طلب رمز جديد.')

    if otp.is_expired():
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        return False, _('انتهت صلاحية رمز التحقق. يرجى طلب رمز جديد.')

    if not verify_hash(code, otp.code_hash):
        return False, _('رمز التحقق غير صحيح.')

    otp.is_used = True
    otp.save(update_fields=['is_used'])

    user.email_verified = True
    user.is_active = True
    user.save(update_fields=['email_verified', 'is_active'])

    return True, _('تم تفعيل الحساب بنجاح')


def send_verification_otp(user):
    remaining = get_resend_cooldown_remaining(user)
    if remaining > 0:
        return None, remaining, {}

    code = create_verification_otp(user)
    delivery_payload = deliver_otp(
        user=user,
        otp_code=code,
        purpose='email_verification',
    )
    return code, 0, delivery_payload
