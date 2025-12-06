from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from apps.exercises.services.exercise_service import ExerciseService

class ExerciseViewSet(ViewSet):
    service = ExerciseService()

    def list(self, request):
        exercises = self.service.get_all()
        return Response(exercises, status=status.HTTP_200_OK)

    def create(self, request):
        exercise = self.service.create(request.data)
        return Response(exercise, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        exercise = self.service.get_by_id(pk)
        return Response(exercise, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        exercise =  self.service.update(pk, request.data)
        return Response(exercise, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.service.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)