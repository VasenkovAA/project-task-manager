from django.db import models
from simple_history.models import HistoricalRecords


class Category(models.Model):
    category_name = models.CharField(
        max_length=255, verbose_name='Category Name', help_text='Enter the name of the category', unique=True
    )
    category_description = models.TextField(
        verbose_name='Category Description',
        help_text='Description of the category',
        blank=True,
    )
    category_settings = models.JSONField(
        verbose_name='Category Settings',
        help_text='JSON configuration for the category',
        default=dict,
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.category_name
