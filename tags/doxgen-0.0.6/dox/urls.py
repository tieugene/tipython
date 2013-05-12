# -*- coding: utf-8 -*-
'''
lansite.apps.core.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('dox.views',
	url(r'^$',				'index'),
	url(r'^(?P<uuid>[0-9A-Z]{32})/$',	'doc_l'),
	url(r'^(?P<uuid>[0-9A-Z]{32})/a/$',	'doc_a'),
	url(r'^(?P<uuid>[0-9A-Z]{32})/c/$',	'doc_c'),
	url(r'^(?P<id>\d+)/u/$',		'doc_u'),
	url(r'^(?P<id>\d+)/r/$',		'doc_r'),
	url(r'^(?P<id>\d+)/p/$',		'doc_p'),
	url(r'^(?P<id>\d+)/v/$',		'doc_v'),
	url(r'^(?P<id>\d+)/d/$',		'doc_d'),
)
