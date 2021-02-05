from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from app_vacancy.forms.myresume import MyResumeForm


class ResumeStartView(View):

    @method_decorator(login_required)
    def get(self, request):
        try:
            if request.user.resumes:
                return redirect('ResumeEditView')
        except ObjectDoesNotExist:
            return render(request, 'myresume/myresume-start.html')


class ResumeCreateView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            if request.user.resumes:
                return redirect('ResumeEditView')
        except ObjectDoesNotExist:
            form = MyResumeForm()
            messages.info(request, 'Please fill the information about you!')
            return render(request, 'myresume/myresume-create.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyResumeForm(request.POST)
        if form.is_valid():
            new_resume = form.save(commit=False)
            new_resume.user = owner
            new_resume.save()
            messages.success(request, 'Congratulations! Resume created!')
            return redirect('ResumeEditView')

        messages.error(request, 'ERROR! Resume not created!')
        return render(request, 'myresume/myresume-create.html', {'form': form})


class ResumeEditView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            my_resume = request.user.resumes
        except ObjectDoesNotExist:
            return redirect('ResumeStartView')
        form = MyResumeForm(instance=my_resume)
        return render(request, 'myresume/myresume-edit.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyResumeForm(request.POST, instance=owner.resumes)
        if form.is_valid():
            my_resume = form.save(commit=False)
            my_resume.user = owner
            my_resume.save()
            messages.success(request, 'Resume updated!')
            return redirect(request.path)

        messages.error(request, 'ERROR! Resume not updated!')
        return render(request, 'myresume/myresume-edit.html', {'form': form})


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 error - server side error (page not found)')


def custom_handler500(request):
    return HttpResponseServerError('500 error - internal server error')
