from django import forms
from task.models.link import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'link_description': forms.Textarea(attrs={'rows': 3}),
            'link_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }

    def clean_link_url(self):
        url = self.cleaned_data['link_url']
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError('URL must start with http:// or https://')
        return url
