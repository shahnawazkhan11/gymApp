from django.test import TestCase
from django.contrib.auth import get_user_model
from exercises.models import Exercise, Template, Session, Set

User = get_user_model()


class ExerciseModelTest(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="Bench Press",
            description="A compound chest exercise",
            bodypart="chest",
            equipment="barbell",
            difficulty="intermediate",
            tags=["compound", "push"],
        )

    def test_exercise_creation(self):
        self.assertEqual(self.exercise.name, "Bench Press")
        self.assertTrue(isinstance(self.exercise.tags, list))
        self.assertEqual(len(self.exercise.tags), 2)

    def test_exercise_str_representation(self):
        self.assertEqual(str(self.exercise), "Bench Press")


class TemplateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.exercise = Exercise.objects.create(
            name="Bench Press",
            bodypart="chest",
            equipment="barbell",
            difficulty="intermediate",
        )
        self.template = Template.objects.create(name="Push Day", user=self.user)
        self.template.exercises.add(self.exercise)

    def test_template_creation(self):
        self.assertEqual(self.template.name, "Push Day")
        self.assertEqual(self.template.exercises.count(), 1)
        self.assertEqual(self.template.user, self.user)
