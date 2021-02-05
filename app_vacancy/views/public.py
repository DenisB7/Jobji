import re
from random import sample

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from app_vacancy.forms.application import ApplicationForm
from app_vacancy.models import Company, Specialty, Vacancy


class AboutView(View):

    def get(self, request):
        return render(request, 'public/about.html')


class MainView(View):

    def get(self, request):
        specialties = Specialty.objects.annotate(vacancies_number=Count('vacancies'))
        companies = Company.objects.only('id', 'name', 'logo').annotate(vacancies_number=Count('vacancies'))
        skills = Vacancy.objects.values('skills')
        set_of_skills = set()
        for skills_list in skills:
            skills_split = re.findall('[A-Za-z0-9]+', skills_list['skills'])
            set_of_skills.update(skills_split)
        skills_random = sample(set_of_skills, 5)
        main = {
            'specialties': specialties,
            'companies': companies,
            'skills_random': skills_random,
        }
        return render(request, 'public/main.html', context=main)


class SearchView(View):

    def get(self, request):
        query = request.GET.get('s')
        if query:
            vacancies = (
                Vacancy.objects
                .defer('description')
                .select_related('specialty', 'company')
                .filter(Q(title__icontains=query) | Q(skills__icontains=query))
            )
            if not vacancies:
                vacancies = (
                    Vacancy.objects
                    .defer('description')
                    .select_related('specialty', 'company')
                    .filter(specialty__title__icontains=query)
                )
        else:
            vacancies = Vacancy.objects.defer('description').select_related('specialty', 'company')
        vacancies_length = len(vacancies)
        vacancies_and_query = {
            'vacancies': vacancies,
            'query': query,
            'vacancies_length': vacancies_length,
        }
        return render(request, 'public/search.html', context=vacancies_and_query)


class AllVacanciesView(View):

    def get(self, request):
        vacancies = Vacancy.objects.defer('description').select_related('specialty', 'company')
        vacancies_amount = len(vacancies)
        all_vacancies = {
            'vacancies': vacancies,
            'vacancies_amount': vacancies_amount,
        }
        return render(request, 'public/vacancies.html', context=all_vacancies)


class VacanciesSpecView(View):

    def get(self, request, specialty):
        spec = get_object_or_404(Specialty, code=specialty)
        vacs_of_spec = spec.vacancies.defer('description').select_related('specialty', 'company')
        vacs_of_spec_amount = len(vacs_of_spec)
        vacancies_of_spec = {
            'spec_title': spec.title,
            'vacs_of_spec': vacs_of_spec,
            'vacs_of_spec_amount': vacs_of_spec_amount,
        }
        return render(request, 'public/vacsspec.html', context=vacancies_of_spec)


class AllCompaniesView(View):

    def get(self, request):
        companies = Company.objects.defer('owner')
        companies_amount = len(companies)
        all_companies = {
            'companies': companies,
            'companies_amount': companies_amount,
        }
        return render(request, 'public/companies.html', context=all_companies)


class CompaniesView(View):

    def get(self, request, company_id):
        company = get_object_or_404(Company, id=company_id)
        vacs_of_company = (
            company.vacancies
            .select_related('specialty', 'company')
            .defer('description', 'company__owner')
        )
        vacs_of_company_amount = len(vacs_of_company)
        companies = {
            'company': company,
            'vacs_of_company': vacs_of_company,
            'vacs_of_company_amount': vacs_of_company_amount,
        }
        return render(request, 'public/company.html', context=companies)


class OneVacancyView(View):

    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(
            Vacancy.objects
            .select_related('specialty', 'company')
            .defer('company__owner'), id=vacancy_id)
        company = vacancy.company
        form = ApplicationForm()
        vac_and_form = {
            'vacancy': vacancy,
            'company': company,
            'form': form,
        }
        return render(request, 'public/vacancy.html', context=vac_and_form)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy_id = vacancy_id
            application.user_id = vacancy.company.owner_id
            application.save()
            return redirect('SendRequestView', vacancy_id=vacancy_id)

        company = vacancy.company
        vac_and_form = {
            'vacancy': vacancy,
            'company': company,
            'form': form,
        }
        return render(request, 'public/vacancy.html', context=vac_and_form)


class SendRequestView(View):

    def get(self, request, vacancy_id):
        try:
            Vacancy.objects.get(id=vacancy_id)
        except ObjectDoesNotExist:
            raise Http404
        vacancy_send = {'vacancy_id': vacancy_id}
        return render(request, 'public/sent.html', context=vacancy_send)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 error - server side error (page not found)')


def custom_handler500(request):
    return HttpResponseServerError('500 error - internal server error')
