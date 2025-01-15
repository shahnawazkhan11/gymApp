from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # Import AllowAny instead of IsAuthenticated
from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Change this line to use AllowAny
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return Workout.objects.all()  # Return all workouts instead of filtering by user

    def perform_create(self, serializer):
        # For development, you can either:
        # Option 1: Set a default user
        serializer.save(user_id=1)  # Assuming user with ID 1 exists
        # Option 2: Remove user requirement temporarily if you modified your model