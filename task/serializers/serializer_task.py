from rest_framework import serializers
from task.models import (
    Category,
    Link,
    Location,
    Status,
    Task,
    validate_notifications,
    validate_reminders,
    validate_status_settings,
    validate_time_intervals,
)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with extended functionality."""

    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=True)

    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), allow_null=True)

    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Task._meta.get_field('assignee').remote_field.model.objects.all(), allow_null=True,
    )

    dependencies = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    links = serializers.PrimaryKeyRelatedField(many=True, queryset=Link.objects.all())

    calculated_progress_dependencies = serializers.IntegerField(read_only=True)
    calculated_is_ready = serializers.BooleanField(read_only=True)

    time_intervals = serializers.JSONField(validators=[validate_time_intervals], required=False)
    reminders = serializers.JSONField(validators=[validate_reminders], required=False)
    notifications = serializers.JSONField(validators=[validate_notifications], required=False)
    status_settings = serializers.JSONField(validators=[validate_status_settings], required=False)

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
            'deleted_at',
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
            'is_deleted',
            'estimated_duration',
            'actual_duration',
            'quality_rating',
            'budget',
            'cancel_reason',
            'time_intervals',
            'reminders',
            'repeat_interval',
            'next_activation',
            'tags',
            'notifications',
            'links',
            'task_space',
            'calculated_progress_dependencies',
            'calculated_is_ready',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'deleted_at',
            'author',
            'last_editor',
            'calculated_progress_dependencies',
            'calculated_is_ready',
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
