from apps.exercises.repositories.exercise_repository import ExerciseRepository
from apps.exercises.serializers.exercises_serializer import ExercisesSerializer
from apps.exercises.exeptions import ExerciseNotFoundError

class ExerciseService:
    def __init__(self):
        self.repository = ExerciseRepository()

    def get_all(self):
        exercises = self.repository.get_all()
        return ExercisesSerializer(exercises, many=True).data

    def get_by_id(self, pk):
        exercise = self.get_or_404(pk)
        return ExercisesSerializer(exercise).data

    def create(self, data):
        serializer = ExercisesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        exercise = self.repository.create(serializer.validated_data)
        return ExercisesSerializer(exercise).data

    def update(self, pk, data):
        exercise = self.get_or_404(pk)

        serializer = ExercisesSerializer(exercise, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_exercise = self.repository.update(exercise, serializer.validated_data)
        return ExercisesSerializer(updated_exercise).data

    def delete(self, pk):
        exercise = self.get_or_404(pk)
        self.repository.delete(exercise)

    def get_or_404(self, pk):
        exercise = self.repository.get_by_id(pk)
        if exercise is None:
            raise ExerciseNotFoundError(f"Exercise with id {pk} not found.")
        return exercise





