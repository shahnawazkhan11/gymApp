# workouts/admin.py
from django.contrib import admin
from .models import Workout, WorkoutExercise, WorkoutSet

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'date')
    list_filter = ('user', 'template', 'date')

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout', 'exercise', 'order')
    list_filter = ('workout', 'exercise')

@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout_exercise', 'weight', 'reps', 'completed', 'order')