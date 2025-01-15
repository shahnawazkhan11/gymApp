from rest_framework import serializers
from .models import Exercise, Template, Session, Set

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'