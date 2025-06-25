from django import forms
from django.contrib.auth import get_user_model

from task.models import (
    Link,
    Task,
    TaskLink,
)

User = get_user_model()


class TaskLinkForm(forms.ModelForm):
    class Meta:
        model = TaskLink
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'task': forms.Select(attrs={'class': 'select2'}),
            'link': forms.Select(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.select_related('task_space')
        self.fields['link'].queryset = Link.objects.select_related('link_space')

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('task')
        link = cleaned_data.get('link')

        if task and link and task.task_space != link.link_space:
            self.add_error(None, 'Task and Link must belong to the same Space')

        return cleaned_data
