from django.contrib import admin
from .models import Commission, Comment


class Commentline(admin.TabularInline):
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [Commentline,]


admin.site.register(Commission, CommissionAdmin)
