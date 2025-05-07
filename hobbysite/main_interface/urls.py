from django.urls import path
from .views import AppsListView

urlpatterns = [
    path('', AppsListView.as_view(), name='homepage'),
]

app_name = "main_interface"
