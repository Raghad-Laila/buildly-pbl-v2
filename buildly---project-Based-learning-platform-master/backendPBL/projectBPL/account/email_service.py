import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

OTP_EMAIL_SUBJECTS = {
    'password_reset': 'رمز إعادة تعيين كلمة المرور - Buildly',
    'email_verification': 'رمز تفعيل حسابك - Buildly',
}

OTP_EXPIRY_MINUTES = 10


class EmailDeliveryError(Exception):
    """Raised when OTP email could not be delivered."""


def is_smtp_configured() -> bool:
    return bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)


def _build_otp_message(*, otp_code: str, purpose: str) -> str:
    if purpose == 'password_reset':
        return (
            f'مرحباً،\n\n'
            f'رمز إعادة تعيين كلمة المرور هو: {otp_code}\n\n'
            f'صلاحية الرمز: {OTP_EXPIRY_MINUTES} دقائق.\n'
            f'إذا لم تطلب إعادة التعيين، تجاهل هذه الرسالة.\n\n'
            f'منصة Buildly'
        )

    return (
        f'مرحباً،\n\n'
        f'رمز تفعيل حسابك هو: {otp_code}\n\n'
        f'صلاحية الرمز: {OTP_EXPIRY_MINUTES} دقائق.\n\n'
        f'منصة Buildly'
    )


def send_otp_email(*, user, otp_code: str, purpose: str) -> None:
    if not is_smtp_configured():
        raise EmailDeliveryError('SMTP credentials are not configured')

    subject = OTP_EMAIL_SUBJECTS.get(purpose, 'رمز التحقق - Buildly')
    message = _build_otp_message(otp_code=otp_code, purpose=purpose)

    sent_count = send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    if sent_count != 1:
        raise EmailDeliveryError(f'Failed to send OTP email to {user.email}')

    logger.info('OTP email sent to %s for purpose=%s', user.email, purpose)
