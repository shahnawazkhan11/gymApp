from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from datetime import datetime

User = get_user_model()

signer = TimestampSigner()


def generate_email_verification_token(user):
    return signer.sign(user.email)


def verify_email_verification_token(token, max_age=86400):  # 24 hours
    try:
        email = signer.unsign(token, max_age=max_age)
        return User.objects.get(email=email)
    except (SignatureExpired, BadSignature, User.DoesNotExist):
        return None


def generate_password_reset_token(user):
    return signer.sign(f"{user.email}:{datetime.now().timestamp()}")


def verify_password_reset_token(token, max_age=3600):  # 1 hour
    try:
        value = signer.unsign(token, max_age=max_age)
        email = value.split(":")[0]
        return User.objects.get(email=email)
    except (SignatureExpired, BadSignature, User.DoesNotExist, IndexError):
        return None
