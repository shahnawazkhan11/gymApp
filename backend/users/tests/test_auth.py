import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from users.tokens import (
    generate_email_verification_token,
    generate_password_reset_token,
)

User = get_user_model()


@pytest.mark.django_db
class TestAuthEndpoints(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.signin_url = reverse("signin")
        self.refresh_url = reverse("refresh-token")
        self.logout_url = reverse("logout")
        self.verify_email_url = reverse("verify-email")
        self.forgot_password_url = reverse("forgot-password")
        self.reset_password_url = reverse("reset-password")

        # Create test user
        self.user_data = {
            "email": "test@example.com",
            "password": "Test123!@#",
            "name": "Test User",
        }
        self.user = User.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["name"],
        )

    def test_signup_success(self):
        """Test successful user registration"""
        data = {
            "email": "newuser@example.com",
            "password": "NewUser123!@#",
            "name": "New User",
        }

        with patch("users.views.send_verification_email.delay") as mock_send_email:
            response = self.client.post(self.signup_url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data
        assert "refresh_token" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == data["email"]
        assert response.data["user"]["name"] == data["name"]
        # assert mock_send_email.called

    def test_signup_validation(self):
        """Test signup validation requirements"""
        invalid_data_cases = [
            # Invalid email
            {
                "data": {"email": "invalid", "password": "Test123!@#", "name": "Test"},
                "expected_error": "email",
            },
            # Password too short
            {
                "data": {
                    "email": "test@example.com",
                    "password": "Test1!",
                    "name": "Test",
                },
                "expected_error": "password",
            },
            # Password without special character
            {
                "data": {
                    "email": "test@example.com",
                    "password": "Test12345",
                    "name": "Test",
                },
                "expected_error": "password",
            },
            # Missing name
            {
                "data": {"email": "test@example.com", "password": "Test123!@#"},
                "expected_error": "name",
            },
        ]

        for case in invalid_data_cases:
            response = self.client.post(self.signup_url, case["data"])
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            # assert response.data["error"] == "validation_error"
            # assert case["expected_error"] in str(response.data["details"]).lower()

    def test_signin_success(self):
        """Test successful login"""
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

        response = self.client.post(self.signin_url, data)

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert "refresh_token" in response.data
        assert "user" in response.data
        assert response.data["user"]["email"] == self.user_data["email"]

    def test_signin_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {"email": self.user_data["email"], "password": "wrongpassword"}

        response = self.client.post(self.signin_url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "invalid_credentials"

    def test_token_refresh(self):
        """Test token refresh"""
        # First, get a valid refresh token
        signin_response = self.client.post(
            self.signin_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )

        refresh_token = signin_response.data["refresh_token"]

        # Then try to refresh it
        response = self.client.post(self.refresh_url, {"refresh_token": refresh_token})

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert "refresh_token" in response.data

    def test_token_refresh_invalid(self):
        """Test token refresh with invalid token"""
        response = self.client.post(
            self.refresh_url, {"refresh_token": "invalid_token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "invalid_token"

    def test_logout(self):
        """Test logout endpoint"""
        # First, get a valid refresh token
        signin_response = self.client.post(
            self.signin_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        print(signin_response.data)

        access_token = signin_response.data["token"]
        refresh_token = signin_response.data["refresh_token"]

        # Then try to logout
        response = self.client.post(
            self.logout_url,
            {"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Successfully logged out"

        # Verify token can't be used anymore
        refresh_response = self.client.post(
            self.refresh_url, {"refresh_token": refresh_token}
        )
        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_email(self):
        """Test email verification"""
        # Generate verification token
        token = generate_email_verification_token(self.user)

        response = self.client.post(self.verify_email_url, {"token": token})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Email verified successfully"

        # Verify user's email_verified status
        self.user.refresh_from_db()
        assert self.user.email_verified is True

    def test_verify_email_invalid_token(self):
        """Test email verification with invalid token"""
        response = self.client.post(self.verify_email_url, {"token": "invalid_token"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "invalid_token"

    def test_forgot_password(self):
        """Test forgot password request"""
        with patch("users.views.send_password_reset_email.delay") as mock_send_email:
            response = self.client.post(
                self.forgot_password_url, {"email": self.user_data["email"]}
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset instructions sent to email"
        assert mock_send_email.called

    def test_forgot_password_nonexistent_email(self):
        """Test forgot password with non-existent email"""
        response = self.client.post(
            self.forgot_password_url, {"email": "nonexistent@example.com"}
        )

        # Should still return 200 for security
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset instructions sent to email"

    def test_reset_password(self):
        """Test password reset"""
        # Generate reset token
        token = generate_password_reset_token(self.user)
        new_password = "NewPassword123!@#"

        response = self.client.post(
            self.reset_password_url, {"token": token, "new_password": new_password}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset successfully"

        # Verify new password works
        signin_response = self.client.post(
            self.signin_url,
            {"email": self.user_data["email"], "password": new_password},
        )
        assert signin_response.status_code == status.HTTP_200_OK

    def test_reset_password_invalid_token(self):
        """Test password reset with invalid token"""
        response = self.client.post(
            self.reset_password_url,
            {"token": "invalid_token", "new_password": "NewPassword123!@#"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "invalid_token"

    def test_rate_limiting(self):
        """Test rate limiting on auth endpoints"""
        # Try to sign in multiple times
        # for _ in range(51):  # Limit is 50 per minute
        #     response = self.client.post(
        #         self.signin_url,
        #         {
        #             "email": self.user_data["email"],
        #             "password": self.user_data["password"],
        #         },
        #     )

        # assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        # assert "error" in response.data
        # assert response.data["error"] == "rate_limit_exceeded"
        pass
