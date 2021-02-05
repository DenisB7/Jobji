from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomRegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, label='Name')
    last_name = forms.CharField(max_length=20, label='Surname')
    email = forms.EmailField(label='Email')

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
        )
        labels = {
            'username': 'Login',
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=30, label='Login')

    class Meta:
        fields = (
            'username',
            'password',
        )
