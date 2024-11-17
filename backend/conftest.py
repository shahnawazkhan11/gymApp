import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user
