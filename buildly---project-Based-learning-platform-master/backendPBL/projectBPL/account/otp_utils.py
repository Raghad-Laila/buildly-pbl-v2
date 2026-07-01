import secrets

from django.contrib.auth.hashers import check_password, make_password


def generate_otp_code():
    return f'{secrets.randbelow(1000000):06d}'


def generate_reset_token():
    return secrets.token_urlsafe(32)


def hash_value(value):
    return make_password(value)


def verify_hash(value, value_hash):
    return check_password(value, value_hash)
