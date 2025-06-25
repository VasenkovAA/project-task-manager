from rest_framework import serializers
from task.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
