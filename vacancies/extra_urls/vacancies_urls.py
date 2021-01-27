from django.urls import path

from app_vacancy.views.public import OneVacancyView, VacanciesSpecView, AllVacanciesView
from app_vacancy.views.public import SendRequestView

from app_vacancy.views.public import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', AllVacanciesView.as_view(), name='AllVacanciesView'),
    path('cat/<str:specialty>/', VacanciesSpecView.as_view(), name='VacanciesSpecView'),
    path('<int:vacancy_id>/', OneVacancyView.as_view(), name='OneVacancyView'),
    path('<int:vacancy_id>/sent', SendRequestView.as_view(), name='SendRequestView'),
]
