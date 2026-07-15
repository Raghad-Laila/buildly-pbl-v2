import logging

from django.conf import settings

from .email_service import is_smtp_configured, send_otp_email

logger = logging.getLogger(__name__)


def deliver_otp(*, user, otp_code, purpose):
    """
    Send OTP via Mailtrap SMTP.
    purpose: 'email_verification' | 'password_reset'
    """
    if not is_smtp_configured():
        logger.error('SMTP is not configured. OTP email was not sent to %s', user.email)
        if settings.DEBUG:
            logger.warning(
                'DEBUG OTP for %s (%s): %s',
                user.email,
                purpose,
                otp_code,
            )
        return {'email_sent': False}

    try:
        send_otp_email(user=user, otp_code=otp_code, purpose=purpose)
        return {'email_sent': True}
    except Exception:
        logger.exception('Failed to send OTP email to %s for purpose=%s', user.email, purpose)
        return {'email_sent': False}
