from django.urls import path

from app_vacancy.views.myresume import ResumeStartView, ResumeCreateView, ResumeEditView

from app_vacancy.views.myresume import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', ResumeEditView.as_view(), name='ResumeEditView'),
    path('start', ResumeStartView.as_view(), name='ResumeStartView'),
    path('create', ResumeCreateView.as_view(), name='ResumeCreateView'),
]
