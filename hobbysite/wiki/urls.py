# <appname>/urls.py
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
]

# This might be needed, depending on your Django version
app_name = "wiki"