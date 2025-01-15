from django.contrib import admin
from .models import BodyMeasurement

@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'weight', 'weight_unit')
    list_filter = ('created_at', 'weight_unit')
    search_fields = ('created_at',)