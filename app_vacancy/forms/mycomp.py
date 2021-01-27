from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from app_vacancy.models import Company, Vacancy


class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)
        labels = {
            'name': 'Название компании',
            'logo': 'Логотип',
            'location': 'География',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('logo'),
            ),
            Row(
                Column('employee_count'),
                Column('location'),
            ),
            Row(
                Column('description'),
            ),
            Row(
                Column(Submit('submit', 'Сохранить')),
            ),
        )


class MyCompanyVacanciesCreateEditForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('company', 'published_at')
        labels = {
            'title': 'Название вакансии',
            'specialty': 'Специализация',
            'skills': 'Требуемые навыки',
            'description': 'Описание вакансии',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('specialty'),
            ),
            Row(
                Column('salary_min'),
                Column('salary_max'),
            ),
            Row(
                Column('skills'),
            ),
            Row(
                Column('description'),
            ),
            Row(
                Column(Submit('submit', 'Сохранить')),
            ),
        )
