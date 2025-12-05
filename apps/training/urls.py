from rest_framework.routers import DefaultRouter

from apps.training.views.training_views import WorkOutSessionView

session_router = DefaultRouter()
session_router.register(r'sessions', WorkOutSessionView, basename='session')