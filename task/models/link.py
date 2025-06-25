from django.db import models
from simple_history.models import HistoricalRecords


class Link(models.Model):
    link_title = models.CharField(
        max_length=255, verbose_name='Link Title', help_text='Enter the title or name of the link', unique=True
    )
    link_description = models.TextField(
        verbose_name='Link Description',
        help_text='Description or notes about the link',
        blank=True,
    )
    link_url = models.URLField(verbose_name='URL', help_text='URL address of the material', unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.link_title
