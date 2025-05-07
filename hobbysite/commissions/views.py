from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission
from django.shortcuts import redirect
from .forms import CommissionForm, JobFormSet
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/CommissionList.html' 


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/CommissionDetail.html' 

class CreateCommissionView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_add.html'

    def form_valid(self, form):
        form.instance.commission_author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("commissions:commissionDetail",
                            kwargs={"pk": self.object.pk})

class CommissionUpdateView(UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(self.request.POST, instance=self.object)
        else:
            context['job_formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()  
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()