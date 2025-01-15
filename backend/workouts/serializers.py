from rest_framework import serializers
from .models import Workout, WorkoutExercise, WorkoutSet
from exercises.serializers import ExerciseSerializer, TemplateSerializer

class WorkoutSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSet
        fields = ['id', 'weight', 'reps', 'completed', 'order']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    workout_sets = WorkoutSetSerializer(many=True)
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_detail', 'order', 'workout_sets']

class WorkoutSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True)
    template_detail = TemplateSerializer(source='template', read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'template', 'template_detail', 'date', 'notes', 'workout_exercises']
        read_only_fields = ['user']

    def create(self, validated_data):
        workout_exercises_data = validated_data.pop('workout_exercises')
        workout = Workout.objects.create(**validated_data)

        for workout_exercise_data in workout_exercises_data:
            workout_sets_data = workout_exercise_data.pop('workout_sets')
            workout_exercise = WorkoutExercise.objects.create(
                workout=workout, 
                **workout_exercise_data
            )

            for workout_set_data in workout_sets_data:
                WorkoutSet.objects.create(
                    workout_exercise=workout_exercise,
                    **workout_set_data
                )

        return workout