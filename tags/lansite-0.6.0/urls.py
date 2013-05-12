# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings

admin.autodiscover()

from views import index

urlpatterns = patterns('',
	(r'^$', index),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
	(r'^accounts/login/$', login),
	(r'^logout/$', logout),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	(r'^ref/', include('ref.urls')),
	(r'^gw/', include('gw.urls')),
)
