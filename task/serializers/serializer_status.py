from rest_framework import serializers
from task.models import Status


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for Status model."""

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['id']
