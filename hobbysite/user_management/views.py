from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserForm
from .models import Profile


class UserCreateView(CreateView):
    model = Profile
    form_class = UserForm
    template_name = 'user_management/home.html'
