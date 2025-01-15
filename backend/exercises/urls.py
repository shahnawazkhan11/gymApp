from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, TemplateViewSet, SessionViewSet, SetViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'sets', SetViewSet, basename='set')

urlpatterns = [
    path('', include(router.urls)),
]