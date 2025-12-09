from rest_framework.serializers import ModelSerializer
from apps.routines.models import Workout, WorkoutExercise
from rest_framework import serializers
from apps.exercises.serializers.exercises_serializer import ExercisesSerializer


class WorkoutSerialzier(ModelSerializer):
    class Meta:
        model = Workout
        fields = (
            'id',
            'routine',
            'name',
            'day_order',
        )
        read_only_fields = ('id', 'day_order')

    def validate_day_order(self, value):
        if not (1 <= value <= 7):
            raise serializers.ValidationError("El día de la semana debe estar entre 1 y 7.")
        return value

class WorkoutUpdateSerializer(ModelSerializer):
    class Meta:
        model = Workout
        fields = (
            'name',
            'day_order',
        )

    def validate_day_order(self, value):
        if not (1 <= value <= 7):
            raise serializers.ValidationError("El día de la semana debe estar entre 1 y 7.")
        return value


class WorkoutExerciseSerializer(ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = (
            'id',
            'workout',
            'exercise',
            'order',
            'sets',
            'reps_min',
            'reps_max',
            'rest_time',
            'notes',
        )
        read_only_fields = ('id', 'workout', 'order')


    def validate_notes(self, value):
        if not value:
            return ''
        if len(value) > 255:
            raise serializers.ValidationError("Las notas no pueden exceder los 255 caracteres.")
        return value

    def validate_reps_min(self, value):
        if value < 1:
            raise serializers.ValidationError("Las repeticiones mínimas deben ser al menos 1.")
        return value

    def validate_reps_max(self, value):
        reps_min = self.initial_data.get('reps_min')

        if value < 1:
            raise serializers.ValidationError("Las repeticiones máximas deben ser al menos 1.")

        if reps_min is not None and value < int(reps_min):
            raise serializers.ValidationError(
                "Las repeticiones máximas no pueden ser menores que las mínimas."
            )

        return value

class WorkoutExerciseDetailSerializer(ModelSerializer):
    workout = serializers.PrimaryKeyRelatedField(read_only=True)
    exercise = ExercisesSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = (
            'id',
            'workout',
            'exercise',
            'order',
            'sets',
            'reps_min',
            'reps_max',
            'rest_time',
            'notes',
        )
        read_only_fields = ('id', 'workout', 'order')


class WorkoutExerciseUpdateSerializer(ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = (
            'sets',
            'reps_min',
            'reps_max',
            'rest_time',
            'notes',
        )

    def validate_notes(self, value):
        if not value:
            return ''
        if len(value) > 255:
            raise serializers.ValidationError("Las notas no pueden exceder los 255 caracteres.")
        return value

    def validate_reps_min(self, value):
        if value < 1:
            raise serializers.ValidationError("Las repeticiones mínimas deben ser al menos 1.")
        return value

    def validate_reps_max(self, value):
        reps_min = self.initial_data.get('reps_min')

        if value < 1:
            raise serializers.ValidationError("Las repeticiones máximas deben ser al menos 1.")

        if reps_min is not None and value < int(reps_min):
            raise serializers.ValidationError(
                "Las repeticiones máximas no pueden ser menores que las mínimas."
            )

        return value


class WorkOutDetailSerializer(ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = (
            'id',
            'routine',
            'name',
            'day_order',
            'exercises',
        )
        read_only_fields = ('id',)