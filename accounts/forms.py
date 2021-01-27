from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, label='Имя')
    last_name = forms.CharField(max_length=20, label='Фамилия')
    email = forms.EmailField(label='Адрес электронной почты')

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
