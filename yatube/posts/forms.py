from django import forms

from .models import Comment, Post
from .validators import ValidateTextFieldMixin


class PostForm(forms.ModelForm, ValidateTextFieldMixin):
    """Form for create/edit post."""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm, ValidateTextFieldMixin):
    """Form for create comment."""
    class Meta:
        model = Comment
        fields = ('text',)
