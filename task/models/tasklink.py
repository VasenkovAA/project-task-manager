from django.db import models
from simple_history.models import HistoricalRecords


class TaskLink(models.Model):
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='task_links',
        verbose_name='Task',
    )
    link = models.ForeignKey(
        'Link',
        on_delete=models.CASCADE,
        related_name='task_links',
        verbose_name='Link',
    )
    description = models.TextField(
        verbose_name='Link Description',
        help_text='Description of the link in the context of the task',
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        unique_together = ('task', 'link')

    def __str__(self):
        return f'{self.task} - {self.link}'
