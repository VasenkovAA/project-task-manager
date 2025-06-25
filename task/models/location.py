from django.db import models
from simple_history.models import HistoricalRecords

from task.models.space import Space


class Location(models.Model):
    location_name = models.CharField(
        max_length=255, verbose_name='Location Name', help_text='Enter the name of the location', unique=True
    )
    location_description = models.TextField(
        verbose_name='Location Description',
        help_text='Detailed description of the location',
        blank=True,
    )
    location_address = models.CharField(
        max_length=512,
        verbose_name='Location Address',
        help_text='Physical address of the location',
        blank=True,
    )
    location_space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        help_text='sapce',
        verbose_name='space',
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.location_name
