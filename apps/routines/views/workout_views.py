from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import logging
from apps.routines.services.workout_exercises_service import WorkOutExercisesService
from apps.routines.services.workout_service import WorkOutService

logger = logging.getLogger(__name__)
class WorkOutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    service = WorkOutService()
    workout_exercises_service = WorkOutExercisesService()

    def retrieve(self, request, pk=None):
        workout = self.service.get_by_id(pk=pk, user=request.user)
        return Response(workout, status=status.HTTP_200_OK)

    def create(self, request):
        workout = self.service.create(data=request.data, user=request.user)
        return Response(workout, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        workout = self.service.update(pk=pk, data=request.data, user=request.user)
        return Response(workout, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.service.delete(pk=pk, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get", "post"], url_path="exercises")
    def exercises(self, request, pk=None):
        logger.info("Peticion recibida en /api/workouts/{pk}/exercises/")
        if request.method == "GET":
            logger.info("Peticion recibida en GET")
            exercises = self.workout_exercises_service.get_exercises_by_workout(pk, request.user)
            logger.info(f"Exercises: {exercises}")
            return Response(
                exercises,
                status=status.HTTP_200_OK
            )
        if request.method == "POST":
            return Response(
                self.workout_exercises_service.add_exercise(request.data, pk, request.user),
                status=status.HTTP_201_CREATED
            )
        return None

    @action(
        detail=True,
        methods=["put", "delete"],
        url_path=r"exercises/(?P<workout_exercise_id>[^/.]+)"
    )
    def exercise_detail(self, request, pk=None, workout_exercise_id=None):
        if request.method == "PUT":
            exercise = self.workout_exercises_service.update_exercise(
                request.data, pk, request.user, workout_exercise_id
            )
            return Response(exercise, status=status.HTTP_200_OK)

        if request.method == "DELETE":
            self.workout_exercises_service.delete_exercise(
                pk, request.user, workout_exercise_id
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None



