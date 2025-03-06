from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
