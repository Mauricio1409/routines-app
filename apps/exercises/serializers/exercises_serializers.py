from rest_framework.serializers import ModelSerializer
from apps.exercises.models import Exercises


class ExercisesSerializer(ModelSerializer):
    class Meta:
        model = Exercises
        fields = (
                'id',
                'name',
                'description',
                'video_url',
                'muscle_group',
                'exercise_type',
                'equipment_type'
                )
        read_only_fields = ('id',)