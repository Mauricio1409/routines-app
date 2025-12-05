from rest_framework.routers import DefaultRouter
from apps.users.views.body_metrics_views import BodyMetricsView

metrics_router = DefaultRouter()
metrics_router.register(r'metrics', BodyMetricsView, basename='metrics')