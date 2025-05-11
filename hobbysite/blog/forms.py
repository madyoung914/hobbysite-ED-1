from django import forms
from .models import Article, Comment, ImageGallery


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']


class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ['image', 'description']
