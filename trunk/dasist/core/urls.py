# -*- coding: utf-8 -*-
'''
dasist.core.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
	url(r'^f/$',			'file_list'),
	url(r'^f/(?P<id>\d+)/$',	'file_view'),
	url(r'^f/(?P<id>\d+)/g/$',	'file_get'),
	url(r'^fs/$',			'fileseq_list'),
	url(r'^fs/(?P<id>\d+)/$',	'fileseq_view'),
)
