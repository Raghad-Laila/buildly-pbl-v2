from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, PasswordResetOTP, PasswordResetSession
from .otp_delivery import deliver_otp
from .otp_utils import generate_otp_code, generate_reset_token, hash_value, verify_hash

OTP_EXPIRY_MINUTES = 10
RESEND_COOLDOWN_SECONDS = 60
SESSION_EXPIRY_MINUTES = 15

GENERIC_REQUEST_MESSAGE = _(
    'إذا كان البريد الإلكتروني مسجلاً لدينا، سيتم إرسال رمز التحقق.'
)


def get_password_reset_cooldown_remaining(user):
    latest_otp = (
        PasswordResetOTP.objects
        .filter(user=user)
        .order_by('-created_at')
        .first()
    )
    if not latest_otp:
        return 0

    elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
    remaining = RESEND_COOLDOWN_SECONDS - elapsed
    return max(0, int(remaining))


def create_password_reset_otp(user):
    PasswordResetOTP.objects.filter(
        user=user,
        is_used=False,
    ).update(is_used=True)

    PasswordResetSession.objects.filter(
        user=user,
        is_used=False,
    ).update(is_used=True)

    code = generate_otp_code()
    expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    PasswordResetOTP.objects.create(
        user=user,
        code_hash=hash_value(code),
        expires_at=expires_at,
    )

    return code


def request_password_reset(email):
    """
    طلب إعادة تعيين كلمة المرور.
    يُرجع دائماً رسالة عامة لمنع كشف وجود البريد.
    """
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return {
            'user_found': False,
            'delivery_payload': {},
            'resend_available_in': RESEND_COOLDOWN_SECONDS,
        }

    remaining = get_password_reset_cooldown_remaining(user)
    if remaining > 0:
        return {
            'user_found': True,
            'delivery_payload': {},
            'resend_available_in': remaining,
            'cooldown_active': True,
        }

    code = create_password_reset_otp(user)
    delivery_payload = deliver_otp(
        user=user,
        otp_code=code,
        purpose='password_reset',
    )

    return {
        'user_found': True,
        'delivery_payload': delivery_payload,
        'resend_available_in': RESEND_COOLDOWN_SECONDS,
        'cooldown_active': False,
    }


def verify_password_reset_otp(user, code):
    otp = (
        PasswordResetOTP.objects
        .filter(user=user, is_used=False)
        .order_by('-created_at')
        .first()
    )

    if not otp:
        return False, _('لا يوجد رمز تحقق صالح. يرجى طلب رمز جديد.'), None

    if otp.is_expired():
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        return False, _('انتهت صلاحية رمز التحقق. يرجى طلب رمز جديد.'), None

    if not verify_hash(code, otp.code_hash):
        return False, _('رمز التحقق غير صحيح.'), None

    otp.is_used = True
    otp.save(update_fields=['is_used'])

    PasswordResetSession.objects.filter(
        user=user,
        is_used=False,
    ).update(is_used=True)

    reset_token = generate_reset_token()
    expires_at = timezone.now() + timedelta(minutes=SESSION_EXPIRY_MINUTES)

    PasswordResetSession.objects.create(
        user=user,
        token_hash=hash_value(reset_token),
        expires_at=expires_at,
    )

    return True, _('تم التحقق من الرمز بنجاح. يمكنك الآن إدخال كلمة المرور الجديدة.'), reset_token


def get_user_from_reset_token(reset_token):
    sessions = (
        PasswordResetSession.objects
        .filter(is_used=False)
        .select_related('user')
        .order_by('-created_at')
    )

    for session in sessions:
        if session.is_expired():
            session.is_used = True
            session.save(update_fields=['is_used'])
            continue

        if verify_hash(reset_token, session.token_hash):
            return session

    return None


def reset_password_with_token(reset_token, new_password):
    session = get_user_from_reset_token(reset_token)

    if not session:
        return False, _('رمز إعادة التعيين غير صالح أو منتهي الصلاحية. يرجى البدء من جديد.'), None

    user = session.user
    user.set_password(new_password)
    user.save(update_fields=['password'])

    session.is_used = True
    session.save(update_fields=['is_used'])

    PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)

    return True, _('تمت إعادة تعيين كلمة المرور بنجاح.'), user
