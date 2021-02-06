from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from app_vacancy.views.public import AboutView, AllCompaniesView, CompaniesView, MainView, SearchView

from app_vacancy.views.public import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='MainView'),
    path('about', AboutView.as_view(), name='AboutView'),
    path('search', SearchView.as_view(), name='SearchView'),
    path('companies/', AllCompaniesView.as_view(), name='AllCompaniesView'),
    path('companies/<int:company_id>/', CompaniesView.as_view(), name='CompaniesView'),
    path('vacancies/', include('vacancies.extra_urls.vacancies_urls')),
    path('mycompany/', include('vacancies.extra_urls.mycompany_urls')),
    path('myresume/', include('vacancies.extra_urls.myresume_urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
