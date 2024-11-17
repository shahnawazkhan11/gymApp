from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from exercises.models import Exercise, Template, Session
import json

User = get_user_model()


class ExerciseAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.exercise_data = {
            "name": "Bench Press",
            "description": "A compound chest exercise",
            "bodypart": "chest",
            "equipment": "barbell",
            "difficulty": "intermediate",
            "tags": ["compound", "push"],
        }

        self.exercise = Exercise.objects.create(**self.exercise_data)
        self.url = reverse("exercise-list")

    def test_get_exercise_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_exercise(self):
        new_exercise = {
            "name": "Squat",
            "description": "A compound leg exercise",
            "bodypart": "legs",
            "equipment": "barbell",
            "difficulty": "intermediate",
            "tags": ["compound", "legs"],
        }
        response = self.client.post(self.url, new_exercise, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 2)

    def test_get_exercise_detail(self):
        url = reverse("exercise-detail", kwargs={"pk": self.exercise.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.exercise_data["name"])

    def test_update_exercise(self):
        url = reverse("exercise-detail", kwargs={"pk": self.exercise.pk})
        updated_data = {**self.exercise_data, "name": "Updated Bench Press"}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Bench Press")

    def test_filter_exercises(self):
        response = self.client.get(f"{self.url}?bodypart=chest")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(f"{self.url}?bodypart=legs")
        self.assertEqual(len(response.data["results"]), 0)

    def test_search_exercises(self):
        response = self.client.get(f"{self.url}?search=bench")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
