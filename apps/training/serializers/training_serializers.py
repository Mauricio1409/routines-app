from rest_framework.serializers import ModelSerializer
from apps.training.models import WorkoutSession, ExerciseLog
from rest_framework import serializers

class ExerciseLogSerializer(ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = (
            'id',
            'session',
            'exercise',
            'set_number',
            'weight_kg',
            'reps',
            'rpe',
        )
        read_only_fields = ('id', 'workout_session')

class WorkOutSessionSerializer(ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = (
            'id',
            'user',
            'workout',
            'date',
            'duration',
            'notes',
        )

        read_only_fields = ('id', 'user', 'date')

        def validate_workout(self, value):
            if value is None:
                raise serializers.ValidationError("El campo 'workout' no puede estar vacío.")
            return value

class WorkOutSessionDetailSerializer(ModelSerializer):
    logs = ExerciseLogSerializer(many=True)
    class Meta:
        model = WorkoutSession
        fields = (
            'id',
            'user',
            'workout',
            'date',
            'duration',
            'notes',
            'logs'
        )
        read_only_fields = ('id', 'user', 'date')

