from core.repositories.base_repository import BaseRepository
from apps.training.models import ExerciseLog

class ExerciseLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(ExerciseLog)
        