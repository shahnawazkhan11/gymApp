from django.core.management.base import BaseCommand
from users.models import User
from exercises.models import Exercise, Template, Session, Set


class Command(BaseCommand):
    help = "Seeds the database with initial data for exercises, templates, sessions, and sets."

    def handle(self, *args, **options):
        self.seed_exercises()
        self.seed_templates()
        self.seed_sessions()
        self.seed_sets()
        self.stdout.write(self.style.SUCCESS("Database seeding completed."))

    def seed_exercises(self):

        Exercise.objects.all().delete()
        self.stdout.write("Existing exercises deleted.")

        exercises = [
            {
                "name": "Push Up",
                "description": "A bodyweight exercise that primarily targets the chest and triceps.",
                "bodypart": "Chest",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["strength", "bodyweight"],
            },
            {
                "name": "Deadlift",
                "description": "A compound exercise that targets the posterior chain.",
                "bodypart": "Back",
                "equipment": "Barbell",
                "difficulty": "Advanced",
                "tags": ["strength", "compound"],
            },
            {
                "name": "Bicep Curl",
                "description": "An isolation exercise for the biceps.",
                "bodypart": "Arms",
                "equipment": "Dumbbells",
                "difficulty": "Intermediate",
                "tags": ["isolation", "strength"],
            },
            {
                "name": "Squat",
                "description": "A compound exercise targeting the legs and glutes.",
                "bodypart": "Legs",
                "equipment": "Barbell",
                "difficulty": "Intermediate",
                "tags": ["strength", "compound"],
            },
            {
                "name": "Pull Up",
                "description": "A bodyweight exercise that targets the back and biceps.",
                "bodypart": "Back",
                "equipment": "None",
                "difficulty": "Intermediate",
                "tags": ["strength", "bodyweight"],
            },
            {
                "name": "Bench Press",
                "description": "A compound exercise focusing on the chest, shoulders, and triceps.",
                "bodypart": "Chest",
                "equipment": "Barbell",
                "difficulty": "Intermediate",
                "tags": ["strength", "compound"],
            },
            {
                "name": "Plank",
                "description": "An isometric core exercise that targets the abdominal muscles.",
                "bodypart": "Core",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["stability", "core"],
            },
            {
                "name": "Overhead Press",
                "description": "A compound exercise for shoulders and triceps.",
                "bodypart": "Shoulders",
                "equipment": "Barbell",
                "difficulty": "Intermediate",
                "tags": ["strength", "compound"],
            },
            {
                "name": "Lunges",
                "description": "A lower-body exercise targeting the quadriceps, glutes, and hamstrings.",
                "bodypart": "Legs",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["strength", "bodyweight"],
            },
            {
                "name": "Dumbbell Fly",
                "description": "An isolation exercise for the chest.",
                "bodypart": "Chest",
                "equipment": "Dumbbells",
                "difficulty": "Intermediate",
                "tags": ["strength", "isolation"],
            },
            {
                "name": "Bent-Over Row",
                "description": "A compound exercise for the back.",
                "bodypart": "Back",
                "equipment": "Barbell",
                "difficulty": "Intermediate",
                "tags": ["strength", "compound"],
            },
            {
                "name": "Leg Press",
                "description": "A lower-body exercise performed on a leg press machine.",
                "bodypart": "Legs",
                "equipment": "Machine",
                "difficulty": "Beginner",
                "tags": ["strength", "machine"],
            },
            {
                "name": "Calf Raise",
                "description": "An isolation exercise targeting the calf muscles.",
                "bodypart": "Legs",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["isolation", "strength"],
            },
            {
                "name": "Russian Twist",
                "description": "A core exercise that targets the oblique muscles.",
                "bodypart": "Core",
                "equipment": "None",
                "difficulty": "Intermediate",
                "tags": ["core", "strength"],
            },
            {
                "name": "Side Plank",
                "description": "A stability exercise focusing on the obliques.",
                "bodypart": "Core",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["stability", "core"],
            },
            {
                "name": "Tricep Dip",
                "description": "A bodyweight exercise targeting the triceps.",
                "bodypart": "Arms",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["strength", "bodyweight"],
            },
            {
                "name": "Mountain Climbers",
                "description": "A dynamic bodyweight exercise for the core and cardiovascular system.",
                "bodypart": "Core",
                "equipment": "None",
                "difficulty": "Beginner",
                "tags": ["cardio", "core"],
            },
            {
                "name": "Burpee",
                "description": "A full-body cardio exercise.",
                "bodypart": "Full Body",
                "equipment": "None",
                "difficulty": "Intermediate",
                "tags": ["cardio", "full-body"],
            },
            {
                "name": "Face Pull",
                "description": "An exercise targeting the rear delts and traps.",
                "bodypart": "Shoulders",
                "equipment": "Cable Machine",
                "difficulty": "Intermediate",
                "tags": ["strength", "isolation"],
            },
            {
                "name": "Lat Pulldown",
                "description": "An exercise for developing the lat muscles.",
                "bodypart": "Back",
                "equipment": "Machine",
                "difficulty": "Beginner",
                "tags": ["strength", "machine"],
            },
        ]

        for exercise_data in exercises:
            Exercise.objects.get_or_create(**exercise_data)

        self.stdout.write("Exercises seeded.")

    def seed_templates(self):
        Template.objects.all().delete()
        self.stdout.write("Existing templates deleted.")
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found. Create a user first."))
            return

        exercises = Exercise.objects.all()
        if exercises.count() < 3:
            self.stdout.write(
                self.style.ERROR(
                    "Not enough exercises to create templates. Seed exercises first."
                )
            )
            return

        template_data = {
            "name": "Beginner Full Body Workout",
            "user": user,
        }

        template, created = Template.objects.get_or_create(**template_data)
        template.exercises.set(exercises[:3])
        template.save()

        self.stdout.write("Template seeded.")

    def seed_sessions(self):
        user = User.objects.first()

        Session.objects.all().delete()
        self.stdout.write("Existing sessions deleted.")

        if not user:
            self.stdout.write(self.style.ERROR("No user found. Create a user first."))
            return

        template = Template.objects.first()
        if not template:
            self.stdout.write(
                self.style.ERROR("No template found. Seed templates first.")
            )
            return

        session_data = {
            "user": user,
            "template": template,
            "note": "Felt great during the workout.",
        }

        Session.objects.get_or_create(**session_data)
        self.stdout.write("Session seeded.")

    def seed_sets(self):
        session = Session.objects.first()
        Set.objects.all().delete()
        self.stdout.write("Existing sets deleted.")
        if not session:
            self.stdout.write(
                self.style.ERROR("No session found. Seed sessions first.")
            )
            return

        exercises = Exercise.objects.all()
        if not exercises.exists():
            self.stdout.write(
                self.style.ERROR("No exercises found. Seed exercises first.")
            )
            return

        sets = [
            {"session": session, "exercise": exercises[0], "kg": 50, "reps": 10},
            {"session": session, "exercise": exercises[1], "kg": 70, "reps": 8},
            {"session": session, "exercise": exercises[2], "kg": 15, "reps": 12},
        ]

        for set_data in sets:
            Set.objects.get_or_create(**set_data)

        self.stdout.write("Sets seeded.")
