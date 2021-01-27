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
from app_vacancy.views.query_debugger import query_debugger


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
            messages.success(request, 'Информация о компании обновлена!')
            return redirect(request.path)

        messages.error(request, 'ОШИБКА! Информация о компании не обновлена!')
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
            messages.success(request, 'Поздравляем! Вы создали компанию')
            return redirect('MyCompanyView')

        messages.error(request, 'ОШИБКА! Компания не создана!')
        return render(request, 'mycompany/mycompany-create.html', {'form': form})


class MyCompanyVacanciesView(TestIfUserHasCompanyMixin, View):

    @method_decorator(login_required)
    def get(self, request):
        owner = request.user
        vacancies = (
            Vacancy.objects
            .values('id', 'title', 'salary_min', 'salary_max')
            .filter(company__owner=owner)
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
        return render(request, 'mycompany/mycompany_vacancy-start.html')


class MyCompanyVacancyCreateView(LoginRequiredMixin, TestIfUserHasCompanyMixin, View):

    def get(self, request):
        form = MyCompanyVacanciesCreateEditForm()
        messages.info(request, 'Пожалуйста, заполните информацию о вакансии и сохраните')
        return render(request, 'mycompany/mycompany_vacancy-create.html', {'form': form})

    def post(self, request):
        owner = request.user
        form = MyCompanyVacanciesCreateEditForm(request.POST)
        if form.is_valid():
            vacancy_create = form.save(commit=False)
            vacancy_create.company_id = owner.company.id
            vacancy_create.save()
            messages.success(request, 'Поздравляем! Вы создали вакансию')
            return redirect('MyCompanyVacanciesView')

        messages.error(request, 'ОШИБКА! Вакансия не создана!')
        return render(request, 'mycompany/mycompany_vacancy-create.html', {'form': form})


class MyCompanyOneVacancyView(LoginRequiredMixin, TestIfUserHasCompanyMixin, View):

    def get(self, request, mycomp_vac_id):
        vacancy = get_object_or_404(Vacancy, id=mycomp_vac_id)
        expected_request_company = request.user.company.id
        current_request_company = vacancy.company_id
        if current_request_company != expected_request_company:
            return redirect('MyCompanyVacanciesView')
        form = MyCompanyVacanciesCreateEditForm(instance=vacancy)
        applications = (
            vacancy.applications
            .values('written_username', 'written_phone', 'written_cover_letter')
            .filter(vacancy_id=mycomp_vac_id)
        )
        one_vacancy = {
            'form': form,
            'vacancy_title': vacancy.title,
            'applications': applications,
        }
        return render(request, 'mycompany/mycompany_vacancy-edit.html', context=one_vacancy)

    def post(self, request, mycomp_vac_id):
        company_id = request.user.company.id
        vacancy = Vacancy.objects.get(id=mycomp_vac_id)
        form = MyCompanyVacanciesCreateEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            my_comp_vac = form.save(commit=False)
            my_comp_vac.company_id = company_id
            my_comp_vac.save()
            messages.success(request, 'Поздравляем! Вы обновили информацию о вакансии')
            return redirect(request.path)

        applications = (
            vacancy.applications
            .values('written_username', 'written_phone', 'written_cover_letter')
            .filter(vacancy_id=mycomp_vac_id)
        )
        one_vacancy = {
            'form': form,
            'vacancy_title': vacancy.title,
            'applications': applications,
        }
        messages.error(request, 'ОШИБКА! Информация о вакансии не обновлена!')
        return render(request, 'mycompany/mycompany_vacancy-edit.html', context=one_vacancy)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 ошибка - ошибка на стороне '
                                'сервера (страница не найдена)')


def custom_handler500(request):
    return HttpResponseServerError('внутренняя ошибка сервера')
