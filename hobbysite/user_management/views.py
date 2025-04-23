from django.views.generic.edit import CreateView

from .forms import UserForm
from .models import Profile


class UserCreateView(CreateView):
    model = Profile
    form_class = UserForm
    template_name = 'user_management/profile.html'
