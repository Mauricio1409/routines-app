from rest_framework.routers import DefaultRouter
from apps.routines.views.routine_views import RoutineViewSet
from apps.routines.views.workout_views import WorkOutViewSet, WorkoutExerciseViewSet

routine_router = DefaultRouter()
routine_router.register(r'routines', RoutineViewSet, basename='routines')
routine_router.register(r'workouts', WorkOutViewSet, basename='workouts')
routine_router.register(r'workout-exercises', WorkoutExerciseViewSet, basename='workout-exercises')


