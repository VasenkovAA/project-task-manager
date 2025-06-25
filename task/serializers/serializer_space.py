from rest_framework import serializers
from task.models import Space


class SpaceSerializer(serializers.ModelSerializer):
    """Serializer for Space model."""

    class Meta:
        model = Space
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
