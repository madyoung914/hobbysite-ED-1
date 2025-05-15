from django import forms
from .models import Comment, Thread


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
        widgets = {
            'entry': forms.Textarea()
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['author', 'image']

    image = forms.ImageField(required=False)
