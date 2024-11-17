from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Exercise, Template, Session, Set


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "bodypart",
        "equipment",
        "difficulty",
        "tag_list",
        "usage_count",
    )
    list_filter = ("bodypart", "equipment", "difficulty")
    search_fields = ("name", "description", "tags")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description")}),
        ("Classification", {"fields": ("bodypart", "equipment", "difficulty")}),
        ("Additional Info", {"fields": ("tags",), "classes": ("collapse",)}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            usage_count=Count("template", distinct=True) + Count("set", distinct=True)
        )

    def tag_list(self, obj):
        return format_html(
            '<span style="color: #666;">{}</span>',
            ", ".join(obj.tags) if obj.tags else "-",
        )

    tag_list.short_description = "Tags"

    def usage_count(self, obj):
        return obj.usage_count

    usage_count.short_description = "Times Used"
    usage_count.admin_order_field = "usage_count"


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "exercise_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "user__email", "user__username")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("exercises",)

    def exercise_count(self, obj):
        return obj.exercises.count()

    exercise_count.short_description = "Exercises"


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "template_name",
        "created_at",
        "completed_at",
        "set_count",
    )
    list_filter = ("completed_at", "created_at")
    search_fields = ("user__email", "user__username", "template__name", "note")
    readonly_fields = ("created_at", "updated_at")

    def template_name(self, obj):
        return obj.template.name if obj.template else "-"

    template_name.short_description = "Template"

    def set_count(self, obj):
        return obj.sets.count()

    set_count.short_description = "Sets"


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("id", "session_info", "exercise", "kg", "reps", "created_at")
    list_filter = ("created_at", "exercise")
    search_fields = ("session__user__email", "exercise__name")
    readonly_fields = ("created_at",)

    def session_info(self, obj):
        return f"Session #{obj.session.id} ({obj.session.user.email})"

    session_info.short_description = "Session"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("session", "session__user", "exercise")
        )
