from django.views.generic.list import ListView
from user_management.models import Profile


class AppsListView(ListView):
    model = Profile
    template_name = 'main_interface/homepage.html'
