from django import forms
from task.models.category import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'  # noqa: DJ007
        widgets = {
            'category_description': forms.Textarea(attrs={'rows': 4}),
            'category_settings': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'JSON configuration for category-specific rules'},
            ),
        }

    def clean_category_name(self):
        name = self.cleaned_data['category_name']
        if Category.objects.exclude(pk=self.instance.pk).filter(category_name__iexact=name).exists():
            raise forms.ValidationError('Category name must be unique.')
        return name
