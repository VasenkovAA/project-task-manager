from rest_framework import serializers
from task.models import File


class FileSerializer(serializers.ModelSerializer):
    """Serializer for File model."""

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['id']
