from django.utils.timezone import override

from core.repositories.base_repository import BaseRepository
from apps.routines.models import Workout

class WorkoutRepository(BaseRepository):
    def __init__(self):
        super().__init__(Workout)

    def get_sessions_by_workout(self, workout):
        return workout.sessions.all()

    @override
    def get_by_id(self, pk):
        return (
            Workout.objects
            .select_related("routine")
            .filter(id=pk)
            .first()
        )

    def get_detail_by_id(self, pk):
        return (
            Workout.objects
            .prefetch_related("exercises")
            .select_related("routine")
            .filter(id=pk)
            .first()
        )
