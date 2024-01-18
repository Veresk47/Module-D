from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author','postCategory','title','text']

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get('title')
            text = cleaned_data.get('text')

            if text == title:
                raise ValidationError('Текст не должен быть идентичен заголовку')

            return cleaned_data




