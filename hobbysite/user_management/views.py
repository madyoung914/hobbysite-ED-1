from django.views.generic.detail import DetailView

from .forms import UserForm
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    form_class = UserForm
    template_name = 'user_management/profile.html'

    slug_field = 'user__username'      
    slug_url_kwarg = 'username'

    
