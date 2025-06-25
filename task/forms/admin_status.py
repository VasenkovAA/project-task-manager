from django import forms
from django.core.exceptions import ValidationError
from task.models.status import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = (
            'status_name',
            'status_description',
            'status_settings',
        )
        widgets = {
            'status_name': forms.TextInput(attrs={
                'class': 'vTextField',
                'placeholder': 'e.g., In Progress',
            }),
            'status_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe what this status means',
            }),
            'status_settings': forms.Textarea(attrs={
                'rows': 4,
                'class': 'json-field',
                'placeholder': '{"progress_on_set": 50, "is_completed": false}',
            }),
        }
    def clean_status_name(self):
        name = self.cleaned_data['status_name']
        qs = Status.objects.filter(status_name__iexact=name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError('Status with this name already exists (case-insensitive).')
        return name
