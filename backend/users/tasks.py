from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_verification_email(email, token):
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    send_mail(
        "Verify your email",
        f"Click the following link to verify your email: {verification_url}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@shared_task
def send_password_reset_email(email, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    send_mail(
        "Reset your password",
        f"Click the following link to reset your password: {reset_url}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
