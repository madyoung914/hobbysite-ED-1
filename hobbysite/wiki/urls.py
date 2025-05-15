from django.urls import path
from .views import (ArticleListView, ArticleDetailView, ArticleCreateView,
                    ArticleUpdateView, ImageGalleryView,
                    ImageGalleryUpdateView)

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='articles-list'),
    path('article/<int:pk>', ArticleDetailView.as_view(),
         name='article-detail'),
    path('article/add', ArticleCreateView.as_view(), name='article-add'),
    path('article/<int:pk>/edit', ArticleUpdateView.as_view(),
         name='article-edit'),
    path('article/<int:pk>/upload-image/', ImageGalleryView.as_view(),
         name='image-upload'),
    path('article/image/<int:pk>/edit/', ImageGalleryUpdateView.as_view(),
         name='image-update'),
]

app_name = "wiki"
