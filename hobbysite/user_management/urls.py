from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, ProfileListView

urlpatterns = [
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/<str:username>', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/dashboard/<str:username>', ProfileListView.as_view(), name='profile-dashboard'),    
]

app_name = "user_management"
