from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Exercise
from .serializers import ExerciseSerializer
from .filters import ExerciseFilter


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExerciseFilter
    search_fields = ["name", "description"]
    ordering_fields = ["name", "bodypart", "equipment", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply additional filters if needed
        bodypart = self.request.query_params.get("bodypart", None)
        if bodypart:
            queryset = queryset.filter(bodypart__iexact=bodypart)

        equipment = self.request.query_params.get("equipment", None)
        if equipment:
            queryset = queryset.filter(equipment__iexact=equipment)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def bodyparts(self, request):
        bodyparts = Exercise.objects.values_list("bodypart", flat=True).distinct()
        return Response(list(bodyparts))

    @action(detail=False, methods=["get"])
    def equipment(self, request):
        equipment = Exercise.objects.values_list("equipment", flat=True).distinct()
        return Response(list(equipment))
