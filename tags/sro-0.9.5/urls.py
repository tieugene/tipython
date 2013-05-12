# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login
from django.conf import settings
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from settings import LOGIN_REDIRECT_URL
#from apps.sro2.views import index

handler500 = 'apps.sro2.views.err500'

admin.autodiscover()

from views import index, about

urlpatterns = patterns('',
	(r'^$', 'views.index'),
	(r'^admin/(.*)', admin.site.root),
	(r'^accounts/login/$', login),
	(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': LOGIN_REDIRECT_URL}),  
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
	(r'^about/$', 'sro2.views.about'),
	(r'^ref/', include('apps.ref.urls')),
	(r'^gw/', include('apps.gw.urls')),
	(r'^sro2/', include('apps.sro2.urls')),
    (r'^err', 'apps.sro2.views.err'),
)

try:
	from local_urls import *
except ImportError:
	pass
