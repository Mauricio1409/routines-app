from core.repositories.base_repository import BaseRepository
from apps.routines.models import Workout

class WorkoutRepository(BaseRepository):
    def __init__(self):
        super().__init__(Workout)

    def get_sessions_by_workout(self, workout):
        return workout.sessions.all()

    def get_by_id(self, pk):
        workout = Workout.objects.select_related("routine").filter(id=pk).first()
        return workout

    def get_detail_by_id(self, pk):
        workout =  Workout.objects.prefetch_related("exercises").select_related("routine").filter(id=pk).first()
        return workout

    def add_exercice(self, workout, exercise, order=None):

        workout.save()
        return workout
