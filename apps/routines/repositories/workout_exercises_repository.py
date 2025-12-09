from core.repositories.base_repository import BaseRepository
from ..models import WorkoutExercise

class WorkOutExercisesRepository(BaseRepository):
    def __init__(self):
        super().__init__(WorkoutExercise)

    def get_exercises_by_workout(self, workout):
        return workout.exercises.all()

    def get_workout_exercise_by_id(self, workout, workout_exercise_id):
        return workout.exercises.filter(id=workout_exercise_id).first()
