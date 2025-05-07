from django.contrib import admin
from .models import Commission, Comment, Job, JobApplication


class Commentline(admin.TabularInline):
    model = Comment

class JobInLine(admin.TabularInline):
    model = Job

class JobApplicationInLine(admin.TabularInline):
    model = JobApplication

class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [JobApplicationInLine, ]

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInLine,]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
