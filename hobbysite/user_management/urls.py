from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('profile/', UserCreateView.as_view(), name='profile'),
]

app_name = "user_management"
