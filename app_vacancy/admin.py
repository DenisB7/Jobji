from django.contrib import admin

from app_vacancy.models import Company, Specialty, Vacancy, Application, Resume


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
