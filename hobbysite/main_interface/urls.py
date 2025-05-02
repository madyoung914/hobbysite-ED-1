from django.urls import path
from .views import AppsListView, UserCreateView

urlpatterns = [
    path('', AppsListView.as_view(), name='homepage'),
    path('register', UserCreateView.as_view(), name='register'),
]

app_name = "main_interface"
