from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.routines.services.workout_service import WorkOutService


class WorkOutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    service = WorkOutService()

    def retrieve(self, request, pk=None):
        workout = self.service.get_by_id(pk=pk, user=request.user)
        return Response(workout, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        workout = self.service.create(data=request.data, user=request.user)
        return Response(workout, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        workout = self.service.update(pk=pk, data=request.data, user=request.user)
        return Response(workout, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.service.delete(pk=pk, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)





class WorkoutExerciseViewSet(ViewSet):
    permission_classes = [IsAuthenticated]