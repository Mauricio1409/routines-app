from rest_framework.viewsets import ModelViewSet
from apps.exercises.models import Exercises
from apps.exercises.serializers.exercises_serializers import ExercisesSerializer


class ExercisesViewSet(ModelViewSet):
    queryset = Exercises.objects.all()
    serializer_class = ExercisesSerializer