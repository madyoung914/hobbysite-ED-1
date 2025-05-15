from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission, Job, JobApplication
from django.shortcuts import get_object_or_404, redirect
from .forms import CommissionForm, JobFormSet, JobApplicationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if (self.request.user.is_authenticated):

            user_profile = self.request.user.profile
            created_commissions = Commission.objects.filter(
                author=user_profile)
            job_apps = JobApplication.objects.filter(applicant=user_profile)

            applied_commissions = []
            for apps in job_apps:
                if (not (apps.job.commission in applied_commissions)):
                    applied_commissions.append(apps.job.commission)

            ctx['created_commissions'] = created_commissions
            ctx['applied_commissions'] = applied_commissions

        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if (self.request.user.is_authenticated):
            user_profile = self.request.user.profile
            applied_job_ids = JobApplication.objects.filter(
                applicant=user_profile).values_list('job_id', flat=True)

            manpower_required = 0
            taken_slots = 0

            for job in self.object.jobs.all():
                manpower_required += job.manpower_required
                for job_app in job.job_application.all():
                    if job_app.status == 'A':
                        taken_slots += 1

            avl_slots = manpower_required-taken_slots

            ctx['ManpowerRequired'] = manpower_required
            ctx['AvlSlots'] = avl_slots
            ctx['applied_job_ids'] = set(applied_job_ids)
            ctx['form'] = JobApplicationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = JobApplicationForm(request.POST)

        if form.is_valid():

            user = request.user
            login(request, user)

            application = form.save(commit=False)
            job_id = request.POST.get('job_id')
            application.job = get_object_or_404(Job, id=job_id)
            application.applicant = request.user.profile

            application.status = 'P'

            application.save()
            self.object.save()

            return redirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class JobView(DetailView):
    model = Job
    template_name = 'commissions/job_view.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = JobApplicationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            app_id = request.POST.get('app_id')
            action = request.POST.get('action')

            application = get_object_or_404(JobApplication, id=app_id)

            if (action == 'accept'):
                application.status = 'A'
            elif (action == 'reject'):
                application.status = 'R'

            application.save()

            if (self.object.manpower_required
                    == self.object.job_application.filter(status='A').count()):
                for job_app in self.object.job_application.filter(status='P'):
                    job_app.status = 'R'
                    job_app.save()
                self.object.status = 'F'

            self.object.save()
            commission = self.object.commission

            if (commission.jobs.filter(status='F').count()
                    == commission.jobs.all().count()):
                commission.status = 'F'
                commission.save()

            return redirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context)


class CreateCommissionView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(
                self.request.POST, instance=self.object)
        else:
            context['job_formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user.profile

        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("commissions:commission-detail",
                            kwargs={"pk": self.object.pk})


class CommissionUpdateView(UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(
                self.request.POST, instance=self.object)
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

            comm_full = False
            for job in self.object.jobs.all():
                if job.status != 'F':
                    comm_full = False
                    break
                else:
                    comm_full = True

            if (comm_full):
                self.object.status = 'F'

            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
