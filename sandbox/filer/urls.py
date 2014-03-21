# -*- coding: utf-8 -*-
'''
sandbox.filer.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('filer.views',
	url(r'^f/$',			'file_list'),
	url(r'^f/c/$',			'file_add'),
	url(r'^f/(?P<id>\d+)/r/$',	'file_view'),
	url(r'^f/(?P<id>\d+)/g/$',	'file_get'),
	url(r'^f/(?P<id>\d+)/u/$',	'file_edit'),
	url(r'^f/(?P<id>\d+)/d/$',	'file_del'),
)
