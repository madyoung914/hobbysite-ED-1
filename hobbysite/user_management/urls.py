from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, ProfileTemplateView

urlpatterns = [
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/edit', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<str:username>/dashboard', ProfileTemplateView.as_view(), name='profile-dashboard'),    
]

app_name = "user_management"
