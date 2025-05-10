from django.contrib import admin
from .models import Article, ArticleCategory, Comment, ImageGallery


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [ImageGalleryInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory


class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
