from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Space(models.Model):
    space_name = models.CharField(
        max_length=255, verbose_name='Space Name', help_text='Enter the name of the space', unique=True,
    )
    space_settings = models.JSONField(
        verbose_name='Space Settings',
        help_text='JSON configuration for the space',
        default=dict,
        blank=True,
        null=True,
    )
    space_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='spaces',
        blank=True,
        verbose_name='Space Users',
        help_text='Users who belong to this space',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Created At',
        help_text='The date and time when the space was created',
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.space_name
