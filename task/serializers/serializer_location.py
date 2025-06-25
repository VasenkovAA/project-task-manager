from rest_framework import serializers
from task.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']
