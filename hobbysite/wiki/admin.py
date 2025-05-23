from django.contrib import admin
from .models import Article, ArticleCategory, ImageGallery


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')
    search_fields = ('title',)
    inlines = [ImageGalleryInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
