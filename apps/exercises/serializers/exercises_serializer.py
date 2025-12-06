from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.exercises.models import Exercise

class ExercisesSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description','video_url', 'muscle_group', 'equipment_type', 'exercise_type']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value or value.strip() == "" or len(value) < 3:
            raise serializers.ValidationError("El nombre del ejercicio no puede estar vacío y debe tener minimo 3 caracteres.")
        return value