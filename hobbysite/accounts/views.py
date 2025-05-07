from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from user_management.models import Profile

from .forms import CreateUserForm


class UserCreateView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "register.html"

    def form_valid(self, form):
        new_user = form.save()
        Profile.objects.create(user=new_user, name=new_user.username, email=new_user.email)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("login")