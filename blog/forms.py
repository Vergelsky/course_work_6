from blog.models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                from django.forms import CheckboxInput
                if isinstance(field.widget, CheckboxInput):

                    field.widget.attrs['class'] = 'form-check'

                else:
                    field.widget.attrs['class'] = 'form-control'

