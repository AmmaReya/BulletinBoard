from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Post, Response
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title == text:
            raise ValidationError(
                'Описание не должно быть идентично названию.'
            )
        return cleaned_data


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = [
            'text',
        ]
