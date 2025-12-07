import datetime
from apps.routines.models import Routine
from core.repositories.base_repository import BaseRepository


class RoutineRepository(BaseRepository):
    def __init__(self):
        super().__init__(Routine)

    def get_active(self, filters=None):
        now = datetime.date.today()

        if filters:
            return Routine.objects.filter(**filters, end_date__gte=now)

        return Routine.objects.filter(end_date__gte=now)

    def get_detail_by_id(self, pk):
        return (
            Routine.objects
            .prefetch_related("workouts")
            .filter(id=pk)
            .first()
        )

    def get_workouts_by_routine(self, routine, filters=None):
        if filters:
            return routine.workouts.filter(**filters)
        return routine.workouts.all()

    def get_sessions_by_routine(self, routine_id):

        routine = (
            Routine.objects
            .prefetch_related("workouts__sessions")
            .filter(id=routine_id)
            .first()
        )

        if not routine:
            return None

        sessions = []
        for workout in routine.workouts.all():
            sessions.extend(list(workout.sessions.all()))

        return sessions



