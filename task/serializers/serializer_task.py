from rest_framework import serializers

from task.models import (
    Category,
    Link,
    Location,
    Status,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=True, required=False)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), allow_null=True, required=False)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Task._meta.get_field('assignee').remote_field.model.objects.all(), allow_null=True, required=False
    )
    dependencies = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all(), required=False)
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all(), required=False)
    links = serializers.PrimaryKeyRelatedField(many=True, queryset=Link.objects.all(), required=False)

    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        """Retrieve tag names associated with the task."""
        return list(obj.tags.names())

    class Meta:
        model = Task
        fields = [
            'id',
            'task_name',
            'description',
            'priority',
            'status',
            'progress',
            'created_at',
            'updated_at',
            'start_date',
            'end_date',
            'deadline',
            'dependencies',
            'categories',
            'location',
            'author',
            'last_editor',
            'assignee',
            'complexity',
            'risk_level',
            'is_ready',
            'is_recurring',
            'needs_approval',
            'is_template',
            'estimated_duration',
            'actual_duration',
            'quality_rating',
            'budget',
            'cancel_reason',
            'repeat_interval',
            'next_activation',
            'tags',
            'links',
            'task_space',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'author',
            'last_editor',
        ]

    def create(self, validated_data):
        """Create a new Task instance with nested relationships."""
        dependencies = validated_data.pop('dependencies', [])
        categories = validated_data.pop('categories', [])
        links = validated_data.pop('links', [])

        user = self.context['request'].user
        validated_data['author'] = user

        task = Task.objects.create(**validated_data)

        task.dependencies.set(dependencies)
        task.categories.set(categories)
        task.links.set(links)

        return task

    def update(self, instance, validated_data):
        """Update an existing Task instance with nested relationships."""
        dependencies = validated_data.pop('dependencies', None)
        categories = validated_data.pop('categories', None)
        links = validated_data.pop('links', None)

        user = self.context['request'].user
        instance.last_editor = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if dependencies is not None:
            instance.dependencies.set(dependencies)
        if categories is not None:
            instance.categories.set(categories)
        if links is not None:
            instance.links.set(links)

        instance.save()
        return instance

    def to_internal_value(self, data):
        unknown_fields = set(data.keys()) - set(self.fields.keys())
        for field in unknown_fields:
            data.pop(field, None)
        return super().to_internal_value(data)
