from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='articles-list'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('article/add', ArticleCreateView.as_view(), name='article-add'),
]

app_name = "wiki"


