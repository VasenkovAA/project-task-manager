from django import forms
from task.models.location import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'location_description': forms.Textarea(attrs={'rows': 3}),
            'location_address': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_location_name(self):
        name = self.cleaned_data['location_name']
        if Location.objects.exclude(pk=self.instance.pk).filter(location_name__iexact=name).exists():
            raise forms.ValidationError('Location with this name already exists.')
        return name
