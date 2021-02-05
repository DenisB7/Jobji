import os
from datetime import date

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'vacancies.settings'
django.setup()

from app_vacancy.models import Vacancy
from app_vacancy.models import Company
from app_vacancy.models import Specialty

from data import jobs
from data import companies
from data import specialties

if __name__ == '__main__':

    for spec in specialties:
        specialty = Specialty(
            code=spec['code'],
            title=spec['title'],
        )
        specialty.save()

    for comp in companies:
        company = Company(
            name=comp['title'],
            description=comp['description'],
            employee_count=comp['employee_count'],
            location=comp['location'],
        )
        company.save()

    for job in jobs:
        year = int(job['posted'][:4])
        month = int(job['posted'][5:7])
        day = int(job['posted'][8:10])
        skills_with_dots = ' • '.join(job['skills'].split(', '))
        vacancy = Vacancy(
            title=job['title'],
            description=job['description'],
            salary_min=int(job['salary_from']),
            salary_max=int(job['salary_to']),
            published_at=date(year, month, day),
            skills=skills_with_dots,
            company_id=int(job['company']),
            specialty_id=int(Specialty.objects.get(code=job['specialty']).id),
        )
        vacancy.save()
