from django import forms
from task.models.space import Space


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'space_name': forms.TextInput(attrs={'class': 'vTextField'}),
            'space_settings': forms.Textarea(
                attrs={
                    'class': 'vLargeTextField',
                    'rows': 5,
                    'cols': 80,
                    'placeholder': 'Enter valid JSON configuration',
                },
            ),
        }

    def clean_space_name(self):
        name = self.cleaned_data['space_name']
        if Space.objects.exclude(pk=self.instance.pk).filter(space_name__iexact=name).exists():
            raise forms.ValidationError('Space with this name already exists (case-insensitive check).')
        return name
