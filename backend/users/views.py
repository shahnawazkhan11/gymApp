# apps/users/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from users.serializers import (
    SignUpSerializer,
    SignInSerializer,
    UserSerializer,
    TokenRefreshSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
)
from .tokens import (
    generate_email_verification_token,
    verify_email_verification_token,
    generate_password_reset_token,
    verify_password_reset_token,
)
from .tasks import send_verification_email, send_password_reset_email

User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            # Generate and send verification email
            # verification_token = generate_email_verification_token(user)
            # send_verification_email.delay(user.email, verification_token)

            # Prepare response
            user_serializer = UserSerializer(user)
            response_data = {
                "token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(
                {
                    "error": "validation_error",
                    "message": "Invalid request",
                    "details": e.message_dict,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignInView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            if user:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                return Response(
                    {
                        "token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "user": user_serializer.data,
                    }
                )

            return Response(
                {
                    "error": "invalid_credentials",
                    "message": "Invalid email or password",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "error": "validation_error",
                "message": "Invalid request",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh = RefreshToken(serializer.validated_data["refresh_token"])
                return Response(
                    {"token": str(refresh.access_token), "refresh_token": str(refresh)}
                )
            except Exception:
                return Response(
                    {
                        "error": "invalid_token",
                        "message": "Invalid or expired refresh token",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    throttle_scope = "auth"

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid_token", "message": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]

            try:
                user = verify_email_verification_token(token)
                user.email_verified = True
                user.save()
                return Response({"message": "Email verified successfully"})
            except Exception:
                return Response(
                    {
                        "error": "invalid_token",
                        "message": "Invalid or expired verification token",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                token = generate_password_reset_token(user)
                send_password_reset_email.delay(email, token)
                return Response(
                    {"message": "Password reset instructions sent to email"}
                )
            except User.DoesNotExist:
                # We return success even if email doesn't exist for security
                return Response(
                    {"message": "Password reset instructions sent to email"}
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = verify_password_reset_token(token)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully"})
            except Exception:
                return Response(
                    {
                        "error": "invalid_token",
                        "message": "Invalid or expired reset token",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
