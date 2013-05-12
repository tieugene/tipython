# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin, databrowse
from django.contrib.auth.views import login, logout, logout_then_login
from django.contrib.auth.decorators import login_required
from settings import LOGIN_REDIRECT_URL

import os

admin.autodiscover()

#from views import index, about

urlpatterns = patterns('',
	(r'^$', 'views.index'),
	(r'^accounts/login/$', login),
	(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': LOGIN_REDIRECT_URL}),  
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	(r'^admin_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT}),
#	(r'^admin/(.*)', admin.site.root),
	(r'^my_admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
	(r'^admin/', include(admin.site.urls)),
	(r'^service/$', 'views.service'),
	(r'^about/$', 'views.about'),
)

# autodiscover urls
for i in os.listdir('apps'):
	if (
		(not i.startswith('.')) and
		(os.path.isdir(os.path.join('apps', i))) and
		(os.path.exists(os.path.join('apps', i, 'urls.py')))
	):
		urlpatterns += patterns('', (r'^%s/' % i, include('apps.%s.urls' % i)), )

try:
	from local_urls import *
except	ImportError:
	pass
