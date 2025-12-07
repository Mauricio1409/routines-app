from apps.routines.repositories.routine_repository import RoutineRepository
from apps.routines.serializers.workout_serializer import WorkoutSerialzier
from apps.routines.serializers.routine_serializers import RoutineSerializer, RoutineDetailSerializer
from apps.routines.exception import RoutineNotFoundException, RoutinePermissionDeniedException
from apps.training.serializers.training_serializers import WorkOutSessionSerializer

class RoutineService:
    def __init__(self):
        self.repository = RoutineRepository()

    def get_all(self, user, query_params=None):
        param_map = {
            "name" : "name__icontains",
            "goal" : "goal__iexact",
            "start_date" : "start_date__gte",
            "end_date" : "end_date__lte",
        }

        filters = {
            "user" : user
        }

        inactive = custom_date = False

        if query_params:
            if query_params.get("inactive") == "true":
                inactive = True


            for param, field in param_map.items():
                value = query_params.get(param)
                if param in ("start_date", "end_date") and value:
                    custom_date = True
                if value:
                    filters[field] = value

        if inactive or custom_date:
            routines = self.repository.get_all(filters=filters)
            return RoutineSerializer(routines, many=True).data

        routines = self.repository.get_active(filters=filters if filters else None)
        return RoutineSerializer(routines, many=True).data

    def create(self, data, user):
        serializer = RoutineSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        data = {
            **serializer.validated_data,
            "user": user
        }

        routine = self.repository.create(data)
        return RoutineSerializer(routine).data


    def get_or_404_and_owner(self, pk, user):
        routine = self.repository.get_by_id(pk)
        if not routine:
            raise RoutineNotFoundException(f"Routine with id {pk} not found.")
        if routine.user != user:
            raise RoutinePermissionDeniedException("You don't have permission to access this routine.")
        return routine

    def get_by_id(self, pk, user):
        routine = self.repository.get_detail_by_id(pk)
        if not routine:
            raise RoutineNotFoundException(f"Routine with id {pk} not found.")
        if routine.user != user:
            raise RoutinePermissionDeniedException("You don't have permission to access this routine.")
        return RoutineDetailSerializer(routine).data


    def update(self, pk, data, user):
        routine = self.get_or_404_and_owner(pk, user)

        serializer = RoutineSerializer(routine, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_routine = self.repository.update(routine, serializer.validated_data)
        return RoutineSerializer(updated_routine).data

    def delete(self, pk, user):
        routine = self.get_or_404_and_owner(pk, user)
        self.repository.delete(routine)

    def get_workout_by_routine(self, pk, user, query_params=None):

        filters = {}

        if query_params:
            if query_params.get("name"):
                filters["name__icontains"] = query_params.get("name")
            elif query_params.get("day_order"):
                filters["day_order__iexact"] = query_params.get("day_order")

        routine = self.get_or_404_and_owner(pk, user)
        workouts = self.repository.get_workouts_by_routine(routine, filters=filters if filters else None)
        return WorkoutSerialzier(workouts, many=True).data

    def get_sessions_by_routine(self, pk, user):
        self.get_or_404_and_owner(pk, user)
        sessions = self.repository.get_sessions_by_routine(pk)
        return WorkOutSessionSerializer(sessions, many=True).data







