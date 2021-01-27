from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import MyLoginView, RegisterUserView

from accounts.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('login', MyLoginView.as_view(), name='MyLoginView'),
    path('logout', LogoutView.as_view(), name='LogoutView'),
    path('register', RegisterUserView.as_view(), name='RegisterUserView'),
]
