from rest_framework.serializers import ModelSerializer
from apps.users.models import BodyMetric


class BodyMetricsSerialzier(ModelSerializer):
    class Meta:
        model = BodyMetric
        fields = ['id', 'user', 'weight', 'height', 'date', 'body_fat_percentage']
        read_only_fields = ['id', 'user', 'date']