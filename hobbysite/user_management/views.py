from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserEditForm
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'user_management/profile.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = UserEditForm
    template_name = 'user_management/profile_form.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse_lazy(
            'user_management:profile',
            kwargs={'username': self.object.user.username}
        )


class ProfileListView(ListView):
    model = Profile
    template_name = 'user_management/dashboard.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #?
        return context



