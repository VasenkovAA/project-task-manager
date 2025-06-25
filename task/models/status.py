from django.db import models
from simple_history.models import HistoricalRecords

from task.models.space import Space

from .validations import validate_status_settings


class Status(models.Model):
    status_name = models.CharField(
        max_length=100,
        verbose_name='Status Name',
        help_text='Enter the name of the task status',
        unique=True,
    )
    status_description = models.TextField(
        verbose_name='Status Description',
        help_text='Detailed description of the status',
        blank=True,
    )
    status_settings = models.JSONField(
        verbose_name='Status Settings',
        help_text='JSON configuration for the status',
        default=dict,
        blank=True,
        null=True,
        validators=[validate_status_settings],
    )
    status_space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        help_text='sapce',
        verbose_name='space',
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.status_name
