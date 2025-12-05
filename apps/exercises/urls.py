from rest_framework.routers import DefaultRouter
from apps.exercises.views.exercises_views import ExercisesViewSet

router = DefaultRouter()
router.register(r'exercises', ExercisesViewSet, basename='exercises')
