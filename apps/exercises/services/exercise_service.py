from apps.exercises.repositories.exercise_repository import ExerciseRepository
from apps.exercises.serializers.exercises_serializer import ExercisesSerializer
from apps.exercises.exeptions import ExerciseNotFoundError

class ExerciseService:
    def __init__(self):
        self.repository = ExerciseRepository()

    def get_all(self, query_params=None):
        param_map = {
            "name": "name__icontains",
            "muscle_group": "muscle_group__iexact",
            "equipment_type": "equipment_type__iexact",
            "exercise_type": "exercise_type__iexact",
        }

        filtros = {}

        if query_params:
            for param, field in param_map.items():
                value = query_params.get(param)
                if value:
                    filtros[field] = value

        exercises = self.repository.get_all(filters=filtros if filtros else None)
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





