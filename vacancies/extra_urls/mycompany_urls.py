from django.urls import path

from app_vacancy.views.mycomp import MyCompanyView, MyCompanyStartView, MyCompanyStartCreateView
from app_vacancy.views.mycomp import MyCompanyVacanciesView
from app_vacancy.views.mycomp import MyCompanyVacanciesStartView, MyCompanyVacancyCreateView, MyCompanyOneVacancyView

from app_vacancy.views.mycomp import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MyCompanyView.as_view(), name='MyCompanyView'),
    path('start', MyCompanyStartView.as_view(), name='MyCompanyStartView'),
    path('create', MyCompanyStartCreateView.as_view(), name='MyCompanyStartCreateView'),
    path('vacancies', MyCompanyVacanciesView.as_view(), name='MyCompanyVacanciesView'),
    path('vacancies/start', MyCompanyVacanciesStartView.as_view(), name='MyCompanyVacanciesStartView'),
    path('vacancies/create', MyCompanyVacancyCreateView.as_view(), name='MyCompanyVacancyCreateView'),
    path('vacancies/<int:mycomp_vac_id>/', MyCompanyOneVacancyView.as_view(), name='MyCompanyOneVacancyView'),
]
