from core.repositories.base_repository import BaseRepository
from apps.exercises.models import Exercise

class ExerciseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Exercise)