from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Case, IntegerField, When
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django_currentuser.middleware import get_current_user
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from task.models import (
    Category,
    Link,
    Location,
    Space,
    Status,
)
from task.models.validations import validate_notifications, validate_reminders, validate_time_intervals


class Task(models.Model):
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    task_name = models.CharField(
        max_length=200,
        help_text='Task name (max 200 characters)',
        verbose_name='Task Name',
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        help_text='Detailed task description with formatting support',
        verbose_name='Description',
    )
    priority = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Priority on a 10-point scale (1=lowest, 10=highest)',
        verbose_name='Priority',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Current task status',
        verbose_name='Status',
        db_index=True,
    )
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Completion percentage (0-100%)',
        verbose_name='Progress',
    )
    progress_dependencies = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Dependencies completion percentage (0-100%)',
        verbose_name='Dependencies Progress',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text='Automatically set on task creation',
        verbose_name='Created At',
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Automatically updated on save',
        verbose_name='Updated At',
    )
    start_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Planned start date/time',
        verbose_name='Start Date',
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Planned completion date/time',
        verbose_name='End Date',
    )
    deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Task deadline',
        verbose_name='Deadline',
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        help_text='Automatically set on soft deletion',
        verbose_name='Deleted At',
    )
    dependencies = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='dependent_tasks',
        help_text='Tasks that must be completed BEFORE this one',
        verbose_name='Dependencies',
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        help_text='Task categories',
        verbose_name='Categories',
        related_name='tasks',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Physical task location',
        verbose_name='Location',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        help_text='Task creator',
        verbose_name='Author',
    )
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='edited_tasks',
        blank=True,
        null=True,
        help_text='Last user who modified the task',
        verbose_name='Last Editor',
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        help_text='Primary task executor',
        verbose_name='Assignee',
        db_index=True,
    )
    complexity = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Complexity rating (1-10)',
        verbose_name='Complexity',
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES,
        default='low',
        help_text='Task execution risk assessment',
        verbose_name='Risk Level',
    )
    is_ready = models.BooleanField(
        default=False,
        help_text='Ready for execution (all dependencies completed)',
        verbose_name='Ready',
    )
    is_recurring = models.BooleanField(
        default=False,
        help_text='Recurring task (e.g., daily)',
        verbose_name='Recurring',
    )
    needs_approval = models.BooleanField(
        default=False,
        help_text='Requires manager approval upon completion',
        verbose_name='Requires Approval',
    )
    is_template = models.BooleanField(
        default=False,
        help_text='Use as template for new tasks',
        verbose_name='Template',
    )
    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        help_text='Soft deletion flag',
        verbose_name='Deleted',
        db_index=True,
    )
    estimated_duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Planned execution duration in minutes',
        verbose_name='Estimated Duration',
    )
    actual_duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Actual time spent in minutes',
        verbose_name='Actual Duration',
    )
    quality_rating = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Quality rating (1-5 scale)',
        verbose_name='Quality Rating',
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Allocated budget in system currency',
        verbose_name='Budget',
    )
    cancel_reason = models.TextField(
        blank=True,
        help_text="Cancellation reason (required for 'canceled' status)",
        verbose_name='Cancel Reason',
    )
    time_intervals = models.JSONField(
        default=dict,
        help_text='Execution time ranges in JSON format',
        blank=True,
        null=True,
        verbose_name='Time Intervals',
        validators=[validate_time_intervals],
    )
    reminders = models.JSONField(
        default=dict,
        help_text="Reminders in [{'time': datetime, 'method': id}] format",
        blank=True,
        null=True,
        verbose_name='Reminders',
        validators=[validate_reminders],
    )
    repeat_interval = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Recurrence interval (for recurring tasks)',
        verbose_name='Repeat Interval',
    )
    next_activation = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Next execution date (for recurring tasks)',
        verbose_name='Next Activation',
    )
    tags = TaggableManager(
        blank=True,
        help_text='Tagging system for task categorization',
        verbose_name='Tags',
    )
    history = HistoricalRecords(
        excluded_fields=['is_deleted', 'deleted_at'],
        inherit=True,
        verbose_name='Change History',
    )
    notifications = models.JSONField(
        default=dict,
        blank=True,
        help_text='Task event notification methods',
        verbose_name='Notification Methods',
        validators=[validate_notifications],
    )
    links = models.ManyToManyField(
        Link,
        through='TaskLink',
        blank=True,
        help_text='Related external resources and documents',
        verbose_name='Links',
    )

    task_space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        help_text='sapce',
        verbose_name='space',
    )

    class Meta:
        indexes = [
            models.Index(fields=['is_ready']),
            models.Index(fields=['status']),
            models.Index(fields=['assignee']),
        ]

    def __str__(self):
        return self.task_name

    def save(self, *args, **kwargs):
        """Automatic update of last_editor, version, and status-based progress"""
        if not self._state.adding:
            current_user = get_current_user()
            if current_user and current_user.is_authenticated and not self.last_editor_id and hasattr(self, 'request'):
                self.last_editor = self.request.user

        if self.status_id and self.status != self.__original_status:
            settings = getattr(self.status, 'status_settings', {})
            if 'progress_on_set' in settings and settings['progress_on_set'] is not None:
                self.progress = settings['progress_on_set']

        self.full_clean()
        super().save(*args, **kwargs)

        self.__original_status = self.status

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status
    def clean(self):
        """Validate related dates and cancellation conditions"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date')

        if self.end_date and self.deadline and self.end_date > self.deadline:
            raise ValidationError('End date must be before deadline')

        if self.status and self.status.name.lower() == 'canceled' and not self.cancel_reason:
            raise ValidationError('Cancel reason is required for canceled status')

    @property
    def calculated_progress_dependencies(self):
        """Calculate dependencies progress"""
        deps = self.dependencies.filter(is_deleted=False)
        if not deps.exists():
            return 100

        total_weight = deps.count()
        completed = deps.filter(status__is_completed=True).count()
        return int(completed / total_weight * 100)

    @property
    def calculated_is_ready(self):
        """Dynamic calculation of task readiness"""
        return self.calculated_progress_dependencies == 100  # noqa: PLR2004


@receiver(post_save, sender=Task)
def update_dependent_tasks(sender, instance, **kwargs):
    """
    Updating tasks dependent on the current task
    when its progress changes
    """
    dependent_tasks = Task.objects.filter(dependencies=instance)

    dependent_tasks.update(
        progress_dependencies=Case(
            When(dependencies=None, then=100), default=Avg('dependencies__progress'), output_field=IntegerField(),
        ),
        is_ready=Case(
            When(dependencies=None, then=True),
            default=Avg('dependencies__progress') == 100,  # noqa: PLR2004
            output_field=models.BooleanField(),
        ),
    )


@receiver(m2m_changed, sender=Task.dependencies.through)
def update_on_dependencies_change(sender, instance, action, **kwargs):
    """
    Update task when its dependencies change
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        Task.objects.filter(pk=instance.pk).update(
            progress_dependencies=instance.calculated_progress_dependencies, is_ready=instance.calculated_is_ready,
        )
