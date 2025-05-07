from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission
from django.shortcuts import redirect
from .forms import CommissionForm, JobFormSet
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommissionForm()
        return context



    def post(self, request, *args, **kwargs):
        form = CommissionForm(request.POST)
        if form.is_valid():

            user = request.user
            login(request, user)

            commission = form.save(commit=False)
            commission.commission_author = request.user.profile

            commission.save()
            self.object.save()
            return super().form_valid(form)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

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