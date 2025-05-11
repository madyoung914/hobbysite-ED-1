from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('register', UserCreateView.as_view(), name='register'),
]

app_name = "accounts"
