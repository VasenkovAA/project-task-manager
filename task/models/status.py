from django.db import models
from simple_history.models import HistoricalRecords

class Status(models.Model):
    status_name = models.CharField(
        max_length=100,
        verbose_name="Status Name",
        help_text="Enter the name of the task status",
        unique=True
    )
    status_description = models.TextField(
        verbose_name="Status Description",
        help_text="Detailed description of the status",
        blank=True,
        null=True
    )
    status_settings = models.JSONField(
        verbose_name="Status Settings",
        help_text="JSON configuration for the status",
        default=dict,
        blank=True,
        null=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.status_name
