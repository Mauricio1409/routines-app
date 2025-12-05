from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.users.models import BodyMetric
from apps.users.serializers.metrics_serializers import BodyMetricsSerialzier

class BodyMetricsView(ModelViewSet):
    serializer_class = BodyMetricsSerialzier
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BodyMetric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


