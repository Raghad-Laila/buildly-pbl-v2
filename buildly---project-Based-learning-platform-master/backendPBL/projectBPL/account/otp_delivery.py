from django.conf import settings


def build_dev_otp_payload(otp_code):
    """إرجاع الرمز في الاستجابة أثناء التطوير فقط"""
    if settings.DEBUG and otp_code:
        return {'dev_otp': otp_code}
    return {}


def deliver_otp(*, user, otp_code, purpose):
    """
    توصيل رمز OTP للمستخدم.
    purpose: 'email_verification' | 'password_reset'

    في وضع التطوير: يُعاد الرمز ضمن استجابة الـ API.
    لاحقاً: يمكن استبدال هذا المنطق بإرسال بريد إلكتروني دون تغيير بقية النظام.
    """
    if settings.DEBUG:
        return build_dev_otp_payload(otp_code)

    # نقطة التوسعة المستقبلية لإرسال البريد الإلكتروني
    # send_otp_email(user=user, otp_code=otp_code, purpose=purpose)
    return {}
