from django_filters import rest_framework as filters
from .models import Exercise


class ExerciseFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    bodypart = filters.CharFilter(lookup_expr="iexact")
    equipment = filters.CharFilter(lookup_expr="iexact")
    min_difficulty = filters.CharFilter(field_name="difficulty", lookup_expr="gte")
    max_difficulty = filters.CharFilter(field_name="difficulty", lookup_expr="lte")
    tags = filters.CharFilter(method="tags_filter")

    class Meta:
        model = Exercise
        fields = ["bodypart", "equipment", "difficulty"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | queryset.filter(
            description__icontains=value
        )

    def tags_filter(self, queryset, name, value):
        tags = value.split(",")
        return queryset.filter(tags__contains=tags)
