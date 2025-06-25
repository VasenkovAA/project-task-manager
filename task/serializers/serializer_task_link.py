from rest_framework import serializers
from task.models import TaskLink


class TaskLinkSerializer(serializers.ModelSerializer):
    """Serializer for TaskLink model."""

    class Meta:
        model = TaskLink
        fields = '__all__'
        read_only_fields = ['id']
