from ..serializers.workout_serializer import WorkoutExerciseSerializer, WorkoutExerciseUpdateSerializer, WorkoutExerciseDetailSerializer
from ..services.workout_service import WorkOutService
from ..repositories.workout_exercises_repository import WorkOutExercisesRepository

class WorkOutExercisesService:
    def __init__(self):
        self.workout_exercises_repository = WorkOutExercisesRepository()
        self.workout_service = WorkOutService()

    def add_exercise(self, data, pk, user):
        serializer = WorkoutExerciseSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        workout = self.workout_service.get_or_not_found(pk)

        if workout.routine.user != user:
            raise Exception("You do not have permission to access this workout's exercises.")

        order = workout.exercises.count() + 1

        new_workout_exercises = {
            "workout": workout,
            "order": order,
            **serializer.validated_data
        }

        created_workout_exercises = self.workout_exercises_repository.create(new_workout_exercises)

        return WorkoutExerciseSerializer(created_workout_exercises).data

    def get_exercises_by_workout(self, pk, user):
        workout = self.workout_service.get_or_not_found(pk)
        if workout.routine.user != user:
            raise Exception("You do not have permission to access this workout's exercises.")
        exercises = self.workout_exercises_repository.get_exercises_by_workout(workout)
        return WorkoutExerciseDetailSerializer(exercises, many=True).data

    def update_exercise(self, data, pk, user, workout_exercise_id):
        serializer = WorkoutExerciseUpdateSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        workout = self.workout_service.get_or_not_found(pk)

        if workout.routine.user != user:
            raise Exception("You do not have permission to access this workout's exercises.")

        workout_exercise = self.workout_exercises_repository.get_workout_exercise_by_id(workout, workout_exercise_id)

        if not workout_exercise:
            raise Exception("Exercise not found in this workout.")

        updated_workout_exercise = self.workout_exercises_repository.update(workout_exercise, serializer.validated_data)
        return WorkoutExerciseSerializer(updated_workout_exercise).data

    def delete_exercise(self, pk, user, workout_exercise_id):
        workout = self.workout_service.get_or_not_found(pk)

        if workout.routine.user != user:
            raise Exception("You do not have permission to access this workout's exercises.")

        workout_exercise = self.workout_exercises_repository.get_workout_exercise_by_id(workout, workout_exercise_id)

        if not workout_exercise:
            raise Exception("Exercise not found in this workout.")

        self.workout_exercises_repository.delete(workout_exercise)
        
    def exists_exercise_in_workout(self, workout, exercise):
        return self.workout_exercises_repository.exists_exercise_in_workout(workout, exercise)







