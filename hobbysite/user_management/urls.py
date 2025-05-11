from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
<<<<<<< HEAD
    path('profile', UserCreateView.as_view(), name='profile'),
=======
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/<str:username>', ProfileUpdateView.as_view(), name='profile-edit'),
>>>>>>> 6e8e5e3f35cd8f49718c7549124f99b6721daeb9
]

app_name = "user_management"
