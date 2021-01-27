from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterUserForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'reg_log/login.html'


class RegisterUserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('MainView')
        form = RegisterUserForm()
        return render(request, 'reg_log/register.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MyLoginView')

        return render(request, 'reg_log/register.html', {'form': form})


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 ошибка - ошибка на стороне '
                                'сервера (страница не найдена)')


def custom_handler500(request):
    return HttpResponseServerError('внутренняя ошибка сервера')
