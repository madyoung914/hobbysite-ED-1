from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        exclude = ['job', 'applicant', 'status']


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = '__all__'
        exclude = ['created_on', 'updated_on', 'author']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['created_on', 'status']


JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm, fields=[
        'role', 'manpower_required', 'status'], extra=1, can_delete=True)
