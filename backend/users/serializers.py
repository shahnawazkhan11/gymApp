from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "email_verified", "created_at", "updated_at")
        read_only_fields = ("id", "email_verified", "created_at", "updated_at")


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "name")

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character"
            )
        return value

    def create(self, validated_data):
        name = validated_data.pop("name")
        user = User.objects.create_user(
            username=validated_data["email"],  # Using email as username
            name=name,
            **validated_data
        )
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character"
            )
        return value


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
