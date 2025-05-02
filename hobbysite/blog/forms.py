from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry']


#class RecipeImageForm(forms.ModelForm):
 #   class Meta:
  #      model = RecipeImage
   #     fields = ['image', 'description']