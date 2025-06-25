from rest_framework import serializers

from task.models import (
    Category,
    File,
    Link,
    Location,
    Space,
    Status,
    Task,
    TaskLink,
    validate_notifications,
    validate_reminders,
    validate_status_settings,
    validate_time_intervals,
)


class SpaceSerializer(serializers.ModelSerializer):
    """Serializer for Space model.

    Handles serialization/deserialization of Space objects.
    Includes all fields except those marked as read-only.
    """

    class Meta:
        model = Space
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for Status model.

    Handles serialization/deserialization of Status objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model.

    Handles serialization/deserialization of Location objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']


class LinkSerializer(serializers.ModelSerializer):
    """Serializer for Link model.

    Handles serialization/deserialization of Link objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['id']


class FileSerializer(serializers.ModelSerializer):
    """Serializer for File model.

    Handles serialization/deserialization of File objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model.

    Handles serialization/deserialization of Category objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']


class TaskLinkSerializer(serializers.ModelSerializer):
    """Serializer for TaskLink model.

    Handles serialization/deserialization of TaskLink objects.
    Includes all fields with 'id' marked as read-only.
    """

    class Meta:
        model = TaskLink
        fields = '__all__'
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with extended functionality.

    Handles complex serialization/deserialization of Task objects including:
    - ForeignKey relations (status, location, assignee)
    - Many-to-Many relations (dependencies, categories, links)
    - Calculated fields (progress, readiness)
    - JSON field validation (time_intervals, reminders, etc.)
    - Tag management
    """

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
        """Create a new Task instance with nested relationships.

        Processes:
        - Extracts relationship data (dependencies, categories, links)
        - Sets author from request context
        - Creates task instance
        - Sets many-to-many relationships
        """
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
        """Update an existing Task instance with nested relationships.

        Processes:
        - Extracts relationship data (dependencies, categories, links)
        - Updates last_editor from request context
        - Updates instance attributes
        - Updates many-to-many relationships if provided
        """
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
