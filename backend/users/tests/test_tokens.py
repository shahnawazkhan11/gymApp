import pytest
from django.contrib.auth import get_user_model
from users.tokens import (
    generate_email_verification_token,
    verify_email_verification_token,
    generate_password_reset_token,
    verify_password_reset_token,
)
from time import sleep

User = get_user_model()


# @pytest.mark.django_db
# class TestTokens:
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="test@example.com", email="test@example.com", password="Test123!@#"
#         )

#     def test_email_verification_token(self):
#         """Test email verification token generation and verification"""
#         token = generate_email_verification_token(self.user)
#         verified_user = verify_email_verification_token(token)

#         assert verified_user == self.user

#     def test_email_verification_token_expired(self):
#         """Test expired email verification token"""
#         token = generate_email_verification_token(self.user)
#         # Try to verify with a very short max_age
#         verified_user = verify_email_verification_token(token, max_age=1)
#         sleep(2)  # Wait for token to expire

#         assert verified_user is None

#     def test_password_reset_token(self):
#         """Test password reset token generation and verification"""
#         token = generate_password_reset_token(self.user)
#         verified_user = verify_password_reset_token(token)

#         assert verified_user == self.user

#     def test_password_reset_token_expired(self):
#         """Test expired password reset token"""
#         token = generate_password_reset_token(self.user)
#         # Try to verify with a very short max_age
#         verified_user = verify_password_reset_token(token, max_age=1)
#         sleep(2)  # Wait for token to expire

#         assert verified_user is None
