from django.urls import path
from .views import (
    SignUpView,
    SignInView,
    TokenRefreshView,
    LogoutView,
    VerifyEmailView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
