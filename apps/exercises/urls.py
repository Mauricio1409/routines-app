from rest_framework.routers import DefaultRouter
from apps.exercises.views.exercise_views import ExerciseViewSet

exercises_router = DefaultRouter()
exercises_router.register(r'exercises', ExerciseViewSet, basename='exercises')