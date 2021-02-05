from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from app_vacancy.models import Company, Vacancy


class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)
        labels = {
            'name': 'Company title',
            'logo': 'Logo',
            'location': 'Location',
            'description': 'Description of company',
            'employee_count': 'Amount of employees',
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
                Column(Submit('submit', 'Submit')),
            ),
        )


class MyCompanyVacanciesCreateEditForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('company', 'published_at')
        labels = {
            'title': 'Vacancy title',
            'specialty': 'Specialization',
            'skills': 'Required skills',
            'description': 'Description of vacancy',
            'salary_min': 'Salary from',
            'salary_max': 'Salary up to',
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
                Column(Submit('submit', 'Submit')),
            ),
        )
