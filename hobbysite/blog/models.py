from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True
        ) 
    entry = models.TextField()
    #createdOn = date time field only gets set when the model is created
    #updatedOn = date time field always updates on last model update
    #should be sorted by date created in descending order

    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.pk])

    def __str__(self):
        return self.title

