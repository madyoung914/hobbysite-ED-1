from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/edit', ProfileUpdateView.as_view(), name='profile-edit'),
]

app_name = "user_management"
