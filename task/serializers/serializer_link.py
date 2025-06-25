from rest_framework import serializers
from task.models import Link


class LinkSerializer(serializers.ModelSerializer):
    """Serializer for Link model."""

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['id']
