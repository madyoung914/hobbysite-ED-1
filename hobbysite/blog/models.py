from django.db import models
from django.urls import reverse
from user_management import models as userModels


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        userModels.Profile,
        on_delete=models.SET_NULL,
        null=True
        )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True
        )
    #header_image
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.pk])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']

class Comment(models.Model):
    author = models.ForeignKey(
        userModels.Profile,
        on_delete=models.SET_NULL,
        null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog:comment', args=[self.pk])

    def __str__(self):
        return self.author

    class Meta:
        ordering = ['created_on']
