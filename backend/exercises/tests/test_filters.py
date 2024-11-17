from django.test import TestCase
from exercises.filters import ExerciseFilter
from exercises.models import Exercise


class ExerciseFilterTest(TestCase):
    def setUp(self):
        self.exercise1 = Exercise.objects.create(
            name="Bench Press",
            description="Chest exercise",
            bodypart="chest",
            equipment="barbell",
            difficulty="intermediate",
            tags=["compound", "push"],
        )
        self.exercise2 = Exercise.objects.create(
            name="Squat",
            description="Leg exercise",
            bodypart="legs",
            equipment="barbell",
            difficulty="advanced",
            tags=["compound", "legs"],
        )

    def test_search_filter(self):
        filterset = ExerciseFilter({"search": "bench"}, queryset=Exercise.objects.all())
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs[0], self.exercise1)

    def test_bodypart_filter(self):
        filterset = ExerciseFilter(
            {"bodypart": "chest"}, queryset=Exercise.objects.all()
        )
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs[0], self.exercise1)

    def test_equipment_filter(self):
        filterset = ExerciseFilter(
            {"equipment": "barbell"}, queryset=Exercise.objects.all()
        )
        self.assertEqual(len(filterset.qs), 2)

    def test_tags_filter(self):
        filterset = ExerciseFilter(
            {"tags": "compound,push"}, queryset=Exercise.objects.all()
        )
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs[0], self.exercise1)
