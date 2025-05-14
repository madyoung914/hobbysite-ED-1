from django.db import models
from user_management.models import Profile
from django.urls import reverse


class Commission(models.Model):

    class CommStatus(models.TextChoices):
        OPEN = 'O', 'Open'
        FULL = 'F', 'Full'
        COMPLETE = 'C', 'Complete'
        DISCONTINUED = 'D', 'Discontinued'

    class CommManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().annotate(
                status_order=models.Case(
                    models.When(status=Commission.CommStatus.OPEN,
                                then=models.Value(1)),
                    models.When(status=Commission.CommStatus.FULL,
                                then=models.Value(2)),
                    models.When(status=Commission.CommStatus.COMPLETE,
                                then=models.Value(3)),
                    models.When(
                        status=Commission.CommStatus.DISCONTINUED,
                        then=models.Value(4)),
                    default=models.Value(5),
                    output_field=models.IntegerField(),
                )
            ).order_by('status_order', '-created_on')

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=255,
        choices=CommStatus.choices,
        default=CommStatus.OPEN
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commissions')
    created_on = models.DateTimeField(auto_now_add=True)#
    updated_on = models.DateTimeField(auto_now=True)#

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

    objects = CommManager()


class Job(models.Model):
    class JobStatus(models.TextChoices):
        OPEN = 'O', 'Open'
        FULL = 'F', 'Full'

    class JobManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().annotate(
                status_order=models.Case(
                    models.When(status=Commission.CommStatus.OPEN,
                                then=models.Value(1)),
                    models.When(status=Commission.CommStatus.FULL,
                                then=models.Value(2)),
                    default=models.Value(3),
                    output_field=models.IntegerField(),
                )
            ).order_by('status_order')

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()#
    status = models.CharField(
        max_length=255,
        choices=JobStatus.choices,
        default=JobStatus.OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)#

    objects = JobManager()

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse('commissions:job-detail', args=[self.pk])


class JobApplication(models.Model):

    class AppStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        REJECTED = 'R', 'Rejected'

    class JobAppManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().annotate(
                status_order=models.Case(
                    models.When(status=JobApplication.AppStatus.PENDING,
                                then=models.Value(1)),
                    models.When(status=JobApplication.AppStatus.ACCEPTED,
                                then=models.Value(2)),
                    models.When(status=JobApplication.AppStatus.REJECTED,
                                then=models.Value(3)),
                    default=models.Value(4),
                    output_field=models.IntegerField(),
                )
            ).order_by('status_order', 'applied_on')

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_application'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='job_applications'
    )
    status = models.CharField(
        max_length=255,
        choices=AppStatus.choices,
        default=AppStatus.PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)#

    objects = JobAppManager()
