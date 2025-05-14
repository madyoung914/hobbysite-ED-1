from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    email = models.EmailField()
    profile_image = models.ImageField(
        upload_to='images/user_management/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
