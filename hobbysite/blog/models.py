from django.db import models
from django.urls import reverse
from user_management.models import Profile


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
        Profile,
        on_delete=models.SET_NULL,
        null=True, 
        related_name="blogs"
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
    )
    header_image = models.ImageField(null=False, upload_to='images/blog/')
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
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blog_comment_author"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"

    class Meta:
        ordering = ['created_on']


class ImageGallery(models.Model):
    article = models.ForeignKey(
        Article,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='images/blog/', null=False,)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description
