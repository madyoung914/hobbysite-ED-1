from django import forms
from wiki.models import Comment, Article, ImageGallery


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']


class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ['image', 'description']
