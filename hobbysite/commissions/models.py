from turtle import title
from django.db import models
from user_management.models import Profile
from django.urls import reverse

class Commission(models.Model):
    
    class OrderStatus(models.TextChoices):
        OPEN = 'O', 'Open'
        FULL = 'F', 'Full'
        COMPLETE = 'C', 'Complete'
        Discontinued = 'D', 'Discontinued'
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        choices = OrderStatus.choices,
        default = OrderStatus.OPEN
        )
    peopleRequired = models.IntegerField()
    CreatedOn = models.DateTimeField(auto_now_add=True)
    UpdatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commissionDetail', args=[self.pk])

    class Meta:
        ordering = ['-UpdatedOn']


class Comment(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    CreatedOn = models.DateTimeField(auto_now_add=True)
    UpdatedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-UpdatedOn']

class Job(models.Model):
    class OrderStatus(models.TextChoices):
        OPEN = 'O', 'Open'
        FULL = 'F', 'Full'

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpowerRequired = models.IntegerField()
    status = models.CharField(
        choices = OrderStatus.choices,
        default = OrderStatus.OPEN
        )
    
    def updateStatus(self,numApps):
        if numApps==self.manpowerRequired:
            self.status = self.OrderStatus.FULL
            self.save()
    CreatedOn = models.DateTimeField(auto_now_add=True)
    UpdatedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-UpdatedOn']

class JobApplication(models.Model):
    
    class AppStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        REJECTED = 'R', 'Rejected'

    job = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobApplication'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='jobApplication'
    )
    status = models.CharField(
        choices = AppStatus.choices,
        default = AppStatus.PENDING
        )
    role = models.CharField(max_length=255)
    manpowerRequired = models.IntegerField()
    status = models.CharField(default='Open')
    
    AppliedOn = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-AppliedOn']