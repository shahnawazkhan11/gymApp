from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Exercise, Template, Session, Set
from .serializers import (
    ExerciseSerializer,
    TemplateSerializer,
    SessionSerializer,
    SetSerializer
)

class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]  # Accessible to everyone during development

    def get_queryset(self):
        return Template.objects.all()  # Show all templates

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]  # Accessible to everyone during development

    def get_queryset(self):
        return Session.objects.all()  # Show all sessions

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        session = self.get_object()
        session.completed_at = timezone.now()
        session.save()
        return Response({'status': 'session completed'})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SetViewSet(viewsets.ModelViewSet):
    serializer_class = SetSerializer
    permission_classes = [AllowAny]  # Accessible to everyone during development

    def get_queryset(self):
        return Set.objects.all()  # Show all sets

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]  # Accessible to everyone during development
