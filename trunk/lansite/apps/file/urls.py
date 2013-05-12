# -*- coding: utf-8 -*-
'''
lansite.apps.file.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('apps.file.views',
	(r'^$',				'index'),
	(r'^all/$',            		'file_index'),
	(r'^img/$',			'file_index_img'),
	(r'^add/$',			'file_add'),
	(r'^(?P<object_id>\d+)/$',	'file_detail'),
	(r'^(?P<object_id>\d+)/edit/$',	'file_edit'),
	(r'^(?P<object_id>\d+)/del/$',	'file_del'),
	(r'^(?P<object_id>\d+)/get/$',	'file_dl'),
	(r'^dav/',			'dav'),
)
