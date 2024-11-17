from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exercises"
    verbose_name = "Workout Management"  # This will appear in the admin interface
