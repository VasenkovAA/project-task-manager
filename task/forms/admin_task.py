from django import forms
from django.contrib.auth import get_user_model
from django_currentuser.middleware import get_current_user
from taggit.forms import TagField
from task.models.task import (
    Category,
    Location,
    Status,
    Task,
)

User = get_user_model()


class TaskForm(forms.ModelForm):
    tags = TagField(
        required=False, widget=forms.TextInput(attrs={'class': 'vTextField', 'placeholder': 'comma, separated, tags'}),
    )

    class Meta:
        model = Task
        exclude = ['is_deleted', 'deleted_at', 'history']  # noqa: DJ006
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'vTextField'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'priority': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'complexity': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'progress_dependencies': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_activation': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'cancel_reason': forms.Textarea(attrs={'rows': 2}),
            'time_intervals': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': '{"intervals": [{"start": "2023-01-01T09:00", "end": "2023-01-01T12:00"}]}',
                },
            ),
            'reminders': forms.Textarea(
                attrs={'rows': 3, 'placeholder': '[{"time": "2023-01-01T08:00", "method": "email"}]'},
            ),
            'notifications': forms.Textarea(
                attrs={'rows': 3, 'placeholder': '{"on_create": ["email"], "on_complete": ["slack"]}'},
            ),
            'budget': forms.NumberInput(attrs={'step': 0.01}),
            'quality_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.select_related('status_space')
        self.fields['location'].queryset = Location.objects.select_related('location_space')
        self.fields['categories'].queryset = Category.objects.select_related('category_space')
        self.fields['dependencies'].queryset = Task.objects.filter(is_deleted=False)
        self.fields['assignee'].queryset = User.objects.all()
        self.fields['author'].queryset = User.objects.all()
        self.fields['last_editor'].queryset = User.objects.all()

        current_user = get_current_user()
        if current_user and current_user.is_authenticated:
            if not self.instance.pk:
                self.fields['author'].initial = current_user
                self.fields['last_editor'].initial = current_user

            if not self.initial.get('assignee'):
                self.fields['assignee'].initial = current_user

        if self.instance.pk:
            self.fields['dependencies'].initial = self.instance.dependencies.all()
            self.initial['tags'] = ', '.join(t.name for t in self.instance.tags.all())

        for field in ['start_date', 'end_date', 'deadline', 'next_activation']:
            if self.instance.pk and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        deadline = cleaned_data.get('deadline')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date must be after start date')

        if end_date and deadline and end_date > deadline:
            self.add_error('deadline', 'Deadline must be after end date')

        status = cleaned_data.get('status')
        cancel_reason = cleaned_data.get('cancel_reason')

        if status and status.status_name.lower() == 'canceled' and not cancel_reason:
            self.add_error('cancel_reason', 'Cancel reason is required for canceled status')

        progress_dependencies = cleaned_data.get('progress_dependencies', 0)
        if progress_dependencies < 0 or progress_dependencies > 100:  # noqa: PLR2004
            self.add_error('progress_dependencies', 'Progress must be between 0 and 100')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if 'tags' in self.cleaned_data:
            instance.tags.set(self.cleaned_data['tags'])

        if commit:
            instance.save()
            self.save_m2m()

        return instance
