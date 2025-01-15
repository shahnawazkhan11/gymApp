from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BodyMeasurementViewSet

router = DefaultRouter()
router.register(r'measurements', BodyMeasurementViewSet, basename='bodymeasurement')

urlpatterns = [
    path('', include(router.urls)),
]