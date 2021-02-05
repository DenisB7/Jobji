import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from app_vacancy.forms.mycomp import MyCompanyForm
from app_vacancy.forms.mycomp import MyCompanyVacanciesCreateEditForm
from app_vacancy.models import Vacancy


class TestIfUserHasNoCompanyMixin(UserPassesTestMixin):

    def test_func(self):
        try:
            if self.request.user.company:
                return False
        except ObjectDoesNotExist:
            return True

    def handle_no_permission(self):
        return redirect('MyCompanyView')


class TestIfUserHasCompanyMixin(UserPassesTestMixin):

    def test_func(self):
        try:
            if self.request.user.company:
                return True
        except ObjectDoesNotExist:
            return False

    def handle_no_permission(self):
        return redirect('MyCompanyStartView')


class MyCompanyView(LoginRequiredMixin, TestIfUserHasCompanyMixin, View):

    def get(self, request):
        my_company = request.user.company
        form = MyCompanyForm(instance=my_company)
        return render(request, 'mycompany/mycompany-edit.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyCompanyForm(request.POST, request.FILES, instance=owner.company)
        if form.is_valid():
            my_company = form.save(commit=False)
            my_company.owner = owner
            my_company.save()
            messages.success(request, 'Information about company updated!')
            return redirect(request.path)

        messages.error(request, "ERROR! Information about company not updated!")
        return render(request, 'mycompany/mycompany-edit.html', {'form': form})


class MyCompanyStartView(TestIfUserHasNoCompanyMixin, View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'mycompany/mycompany-start.html')


class MyCompanyStartCreateView(LoginRequiredMixin, TestIfUserHasNoCompanyMixin, View):

    def get(self, request):
        form = MyCompanyForm()
        return render(request, 'mycompany/mycompany-create.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            new_company = form.save(commit=False)
            new_company.owner = owner
            new_company.save()
            messages.success(request, "Congratulations! You created company!")
            return redirect('MyCompanyView')

        messages.error(request, "ERROR! Company not created!")
        return render(request, 'mycompany/mycompany-create.html', {'form': form})


class MyCompanyVacanciesView(TestIfUserHasCompanyMixin, View):

    @method_decorator(login_required)
    def get(self, request):
        owner = request.user
        vacancies = (
            owner.company.vacancies
            .values('id', 'title', 'salary_min', 'salary_max')
            .annotate(applications_number=Count('applications'))
        )
        if not vacancies:
            return redirect('MyCompanyVacanciesStartView')
        mycomp_vacs = {'vacancies': vacancies}
        return render(request, 'mycompany/mycompany_vacancy-list.html', context=mycomp_vacs)


class MyCompanyVacanciesStartView(TestIfUserHasCompanyMixin, View):

    @method_decorator(login_required)
    def get(self, request):
        owner_has_company = request.user.company
        if owner_has_company.vacancies.values('id'):
            return redirect('MyCompanyVacanciesView')
        messages.info(request, 'You have no vacancies yet, but you can create the first one!')
        return render(request, 'mycompany/mycompany_vacancy-start.html')


class MyCompanyVacancyCreateView(LoginRequiredMixin, TestIfUserHasCompanyMixin, View):

    def get(self, request):
        form = MyCompanyVacanciesCreateEditForm()
        messages.info(request, 'Please fill the information about vacancy')
        return render(request, 'mycompany/mycompany_vacancy-create.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyCompanyVacanciesCreateEditForm(request.POST)
        if form.is_valid():
            vacancy_create = form.save(commit=False)
            vacancy_create.skills = ' • '.join(re.findall('[A-Za-z0-9]+', vacancy_create.skills))
            vacancy_create.company_id = owner.company.id
            vacancy_create.save()
            messages.success(request, "Congratulations! You created vacancy!")
            return redirect('MyCompanyVacanciesView')

        messages.error(request, "ERROR! Vacancy not created!")
        return render(request, 'mycompany/mycompany_vacancy-create.html', {'form': form})


class MyCompanyOneVacancyView(LoginRequiredMixin, TestIfUserHasCompanyMixin, View):

    def get(self, request, mycomp_vac_id):
        vacancy = get_object_or_404(Vacancy.objects.select_related('specialty', 'company'), id=mycomp_vac_id)
        expected_request_company = request.user.company.id
        current_request_company = vacancy.company_id
        if current_request_company != expected_request_company:
            return redirect('MyCompanyVacanciesView')
        form = MyCompanyVacanciesCreateEditForm(instance=vacancy)
        applications = (
            vacancy.applications
            .filter(vacancy_id=mycomp_vac_id)
            .values('written_username', 'written_phone', 'written_cover_letter')
        )
        one_vacancy = {
            'form': form,
            'vacancy_title': vacancy.title,
            'applications': applications,
            'applications_length': len(applications),
        }
        return render(request, 'mycompany/mycompany_vacancy-edit.html', context=one_vacancy)

    def post(self, request, mycomp_vac_id):
        company_id = request.user.company.id
        vacancy = Vacancy.objects.get(id=mycomp_vac_id)
        form = MyCompanyVacanciesCreateEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            my_comp_vac = form.save(commit=False)
            my_comp_vac.skills = ' • '.join(re.findall('[A-Za-z0-9]+', my_comp_vac.skills))
            my_comp_vac.company_id = company_id
            my_comp_vac.save()
            messages.success(request, 'Information about vacancy updated!')
            return redirect(request.path)

        applications = (
            vacancy.applications
            .filter(vacancy_id=mycomp_vac_id)
            .values('written_username', 'written_phone', 'written_cover_letter')
        )
        one_vacancy = {
            'form': form,
            'vacancy_title': vacancy.title,
            'applications': applications,
            'applications_length': len(applications),
        }
        messages.error(request, "ERROR! Information about vacancy not updated!")
        return render(request, 'mycompany/mycompany_vacancy-edit.html', context=one_vacancy)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 error - server side error (page not found)')


def custom_handler500(request):
    return HttpResponseServerError('500 error - internal server error')
