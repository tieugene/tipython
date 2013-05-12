# -*- coding: utf-8 -*-
'''
lansite.gw.file.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.file.views',
	(r'^file/$',				'file_index'),
	(r'^file/all/$',            		'file_index_all'),
	(r'^file/img/$',			'file_index_img'),
	(r'^file/add/$',			'file_add'),
	(r'^file/view/(?P<item_id>\d+)/$',	'file_detail'),
	(r'^file/edit/(?P<item_id>\d+)/$',	'file_edit'),
	(r'^file/del/(?P<item_id>\d+)/$',	'file_del'),
	(r'^file/get/(?P<item_id>\d+)/$',	'file_dl'),
)
