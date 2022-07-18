"""
urls
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    path('core/', include('core.urls')),
    path('contrib/', include('contrib.urls')),
    path('invoice/', include('invoice.urls')),
    path('contract/', include('contract.urls')),
    #path('invarch/', include('invarch.urls')),
    #path('contrarch/', include('contrarch.urls')),
    #path('report/', include('reports.urls')),
    path('chk/', views.chk, name='chk'),
    path('cln/<int:f>/', views.cln, name='cln'),
]

urlpatterns += staticfiles_urlpatterns()
