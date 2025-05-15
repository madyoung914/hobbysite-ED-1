from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    display_name = forms.CharField(max_length=63)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
