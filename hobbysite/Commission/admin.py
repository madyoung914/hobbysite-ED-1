from django.contrib import admin
from .models import Commission, Comment

class Commentline(admin.TabularInline):
    model = Comment

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [Commentline,]
# Register your models here.

admin.site.register(Commission, CommissionAdmin)