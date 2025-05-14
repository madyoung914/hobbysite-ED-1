from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserEditForm
from .models import Profile
from merchstore.models import Transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'user_management/profile.html'

    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        ctx['profile_user'] = get_object_or_404(User, username=username)
        
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            ctx['threads'] = profile.threads.all()
            ctx['buyerTransactions'] = profile.transactions.all()
            ctx['sellerTransactions'] = Transaction.objects.filter(product__owner=profile)
            ctx['blogs'] = profile.blogs.all()
            ctx['wikis'] = profile.wikis.all()
            ctx['commissionsCreated'] = profile.commissions.all()
            ctx['jobsJoined'] = profile.JobApplications.all()
        return ctx


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


class ProfileTemplateView(TemplateView):
    template_name = 'user_management/dashboard.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['threads'] = profile.threads.all()
        context['buyerTransactions'] = profile.transactions.all()
        context['sellerTransactions'] = Transaction.objects.filter(product__owner=profile)
        context['blogs'] = profile.blogs.all()
        context['wikis'] = profile.wikis.all()
        context['commissionsCreated'] = profile.commissions.all()
        context['jobsJoined'] = profile.JobApplications.all()
        return context


