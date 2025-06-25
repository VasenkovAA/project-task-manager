from django import forms
from task.models.file import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'file_description': forms.Textarea(attrs={'rows': 3}),
        }

    ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'png']

    def clean_file_upload(self):
        file = self.cleaned_data['file_upload']
        extension = file.name.split('.')[-1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise forms.ValidationError(f"Unsupported file extension. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}")

        # 10MB limit
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size exceeds 10MB limit')

        return file
