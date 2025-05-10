from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        exclude = ['job','applicant','status' ]

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = '__all__'
        exclude = ['createdOn','updatedOn','author' ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['createdOn', ]

JobFormSet = inlineformset_factory(Commission, Job, form = JobForm, fields=['role', 'manpowerRequired', 'status'], extra=1, can_delete=True)
