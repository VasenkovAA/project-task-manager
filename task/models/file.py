from django.db import models
from simple_history.models import HistoricalRecords

class File(models.Model):
    file_name = models.CharField(
        max_length=255,
        verbose_name="File Name",
        help_text="Enter the name of the file",
        unique=True
    )
    file_description = models.TextField(
        verbose_name="File Description",
        help_text="Detailed description of the file",
        blank=True,
        null=True
    )
    file_upload = models.FileField(
        upload_to='uploads/files/',
        verbose_name="File Upload",
        help_text="Upload the document file"
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.file_name
