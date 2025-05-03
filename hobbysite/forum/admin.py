from django.contrib import admin
from .models import Thread, ThreadCategory


class ThreadInline(admin.TabularInline):
    model = Thread


class ThreadAdmin(admin.ModelAdmin):
    model = Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    inlines = [ThreadInline]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin)
