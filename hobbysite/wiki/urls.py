from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('wiki/articles', ArticleListView.as_view(), name='articles-list'),
    path('wiki/article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
]

app_name = "wiki"
