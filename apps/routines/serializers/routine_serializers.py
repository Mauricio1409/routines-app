from rest_framework.serializers import ModelSerializer
from apps.routines.models import Routine
from rest_framework import serializers
from apps.routines.serializers.workout_serializer import WorkoutSerialzier


class RoutineSerializer(ModelSerializer):
    class Meta:
        model = Routine
        fields = (
                'id',
                'user',
                'name',
                'description',
                'goal',
                'start_date',
                'end_date',
                )
        read_only_fields = ('id', 'user')

        def validate_goal(self, value):
            valid_goals = [choice[0] for choice in Routine.Goal.choices]
            if value not in valid_goals:
                raise serializers.ValidationError("Objetivo de rutina no válido.")
            return value


class RoutineDetailSerializer(ModelSerializer):
    workouts = WorkoutSerialzier(many=True)
    class Meta:
        model = Routine
        fields = (
                'id',
                'user',
                'name',
                'description',
                'goal',
                'start_date',
                'end_date',
                'workouts',
                )
        read_only_fields = ('id', 'user')

        def validate_goal(self, value):
            valid_goals = [choice[0] for choice in Routine.Goal.choices]
            if value not in valid_goals:
                raise serializers.ValidationError("Objetivo de rutina no válido.")
            return value

