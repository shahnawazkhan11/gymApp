from django.db import models
from django.utils import timezone

class BodyMeasurement(models.Model):
    # Main fields
    created_at = models.DateTimeField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    weight_unit = models.CharField(max_length=2, default='kg')
    
    # Body measurements (all in inches)
    neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulders = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_tricep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_tricep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_forearm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_forearm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_abs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Measurements taken on {self.created_at.strftime('%Y-%m-%d')}"