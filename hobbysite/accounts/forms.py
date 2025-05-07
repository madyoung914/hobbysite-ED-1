from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

=======


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
>>>>>>> 4d69ea7 (added the last feature of merchstore)
