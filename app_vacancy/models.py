from django.db import models
from django.contrib.auth import get_user_model

from vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=150)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.PositiveIntegerField()
    owner = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=12)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=29)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.CharField(max_length=50)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, null=True, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    salary = models.PositiveIntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resumes')
    grade = models.CharField(max_length=50)
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField()

    def __str__(self):
        return self.name
