"""kupa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/',		include(admin.site.urls)),
    url(r'^admin/jsi18n',	'django.views.i18n.javascript_catalog'), # hack to use admin form widgets
    url(r'^accounts/login/$',	login),
    url(r'^logout$',		logout),
    url(r'^about$',		TemplateView.as_view(template_name='about.html'), name='about'),
    #url(r'^$',			include('medrec.urls')),
    #url(r'^$',			TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$',			'medrec.views.index'),
    url(r'^c/a/$',		'medrec.views.client_add'),
    url(r'^c/(?P<pk>\d+)/$',	'medrec.views.client_view'),
    url(r'^c/(?P<pk>\d+)/u/$',	'medrec.views.client_edit'),
    url(r'^c/(?P<pk>\d+)/d/$',	'medrec.views.client_del'),
    url(r'^c/f/(?P<abc>\d+)/$',	'medrec.views.client_set_filter_abc'),
    url(r'^c/s/(?P<sort>\d+)/$','medrec.views.client_set_sort'),
    url(r'^r/(?P<pk>\d+)/$',	'medrec.views.record_view'),
    url(r'^r/(?P<pk>\d+)/u/$',	'medrec.views.record_edit'),
    url(r'^r/(?P<pk>\d+)/d/$',	'medrec.views.record_del'),
    url(r'^r/d/$',		'medrec.views.record_set_date'),
    url(r'^r/d/(?P<date>\d+)/$','medrec.views.record_get_date'),
    url(r'^i/(?P<pk>\d+)/(?P<img>.+)$','medrec.views.img_view'),
    url(r'^i/d/(?P<pk>\d+)/(?P<img>.+)$','medrec.views.img_del'),
]
#urlpatterns += staticfiles_urlpatterns()
