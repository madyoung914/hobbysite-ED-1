from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy

from .models import Article, Profile


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            user_articles = Article.objects.filter(author=profile)
            other_articles = Article.objects.exclude(author=profile)
        else:
            user_articles = Article.objects.none()
            other_articles = Article.objects.all()

        articles_by_category = {}
        for article in other_articles:
            category = article.category #gets the category
            if category not in articles_by_category: #checks if category was already stated
                articles_by_category[category] = [] #creates new list for a new category if category was not already stated
            articles_by_category[category].append(article)

        context['user_articles'] = user_articles
        context['articles_by_category'] = articles_by_category
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'

