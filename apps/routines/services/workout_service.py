from apps.routines.repositories.workout_repository import WorkoutRepository
from .routine_service import RoutineService
from ..exception import RoutinePermissionDeniedException, WorkoutNotFoundException
from ..serializers.workout_serializer import WorkoutSerialzier, WorkoutUpdateSerializer, WorkOutDetailSerializer


class WorkOutService:
    def __init__(self):
        self.repository = WorkoutRepository()
        self.routine_service = RoutineService()

    def create(self, data, user):
        serializer = WorkoutSerialzier(data=data)
        serializer.is_valid(raise_exception=True)

        routine = serializer.validated_data.get("routine")
        if routine.user != user:
            raise RoutinePermissionDeniedException("You do not have permission to add workouts to this routine.")
        day_order = routine.workouts.count() + 1

        data = {
            **serializer.validated_data,
            "day_order": day_order

        }

        workout = self.repository.create(data)
        return WorkoutSerialzier(workout).data

    def get_or_not_found(self, pk):
        workout = self.repository.get_by_id(pk)
        if not workout:
            raise WorkoutNotFoundException(f"Workout with id {pk} not found.")
        return workout

    def update(self, pk, data, user):
        workout = self.get_or_not_found(pk)

        if workout.routine.user != user:
            raise RoutinePermissionDeniedException("You do not have permission to update this workout.")

        serializer = WorkoutUpdateSerializer(workout, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_workout = self.repository.update(workout, serializer.validated_data)
        return WorkoutSerialzier(updated_workout).data

    def get_by_id(self, pk, user):
        workout = self.repository.get_detail_by_id(pk)

        if not workout:
            raise WorkoutNotFoundException(f"Workout with id {pk} not found.")

        if workout.routine.user != user:
            raise RoutinePermissionDeniedException("You do not have permission to access this workout.")
        return WorkOutDetailSerializer(workout).data

    def delete(self, pk, user):
        workout = self.get_or_not_found(pk)

        if workout.routine.user != user:
            raise RoutinePermissionDeniedException("You do not have permission to delete this workout.")

        self.repository.delete(workout)









