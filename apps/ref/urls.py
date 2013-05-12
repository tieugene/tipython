# -*- coding: utf-8 -*-
'''
REF URLs
'''
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *

urlpatterns = patterns('ref.views',
	(r'^$',				'index'),
	(r'^kladr/$',			'kladr_list'),
	(r'^kladr/(?P<item_id>\d+)/$',	'kladr_view'),
	(r'^okato/$',			'okato_list'),
	(r'^okato/(?P<item_id>\d+)/$',	'okato_view'),
	(r'^okopf/$',			'okopf_list'),
	(r'^okopf/(?P<item_id>\d+)/$',	'okopf_view'),
	(r'^oksm/$',			'oksm_list'),
)
