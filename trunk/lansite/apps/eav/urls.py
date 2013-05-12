# -*- coding: utf-8 -*-
'''
lansite.apps.eav.urls
Need:
	* entitytype_list
		* entitytype_detail
			* attribute_list
			* attribute_add
			* attribute_del
			* entity_list
	* entity_list
		* entity_detail
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('apps.eav.views',
	(r'^$',							'index'),
	(r'^entity/$',						'entity_list'),
	(r'^entity/add/$',					'entity_add'),
	(r'^entity/(?P<obj_id>\d+)/(?P<type_id>\d+)/add$',	'entity_add_instant'),
	(r'^entity/(?P<object_id>\d+)/$',			'entity_detail'),
	(r'^entity/(?P<object_id>\d+)/edit/$',			'entity_edit'),
	(r'^entity/(?P<object_id>\d+)/del/$',			'entity_del'),
	(r'^search/$',						'eav_search'),
	(r'^attribute/add/$',					'attribute_add'),
	(r'^attribute/(?P<object_id>\d+)/del/$',		'attribute_del'),
	(r'^entitytype/add/$',					'entitytype_add'),
	(r'^attach/(?P<object_id>\d+)/$',			'eav_attach'),
	(r'^value/(?P<object_id>\d+)/add/$',			'value_add'),
	(r'^value/(?P<object_id>\d+)/del/(?P<tag_id>\d+)/$',	'value_del'),
	(r'^getinput/(?P<object_id>\d+)/$',			'eav_get_input'),
	(r'^ctype/$',						'eav_ctype'),
	(r'^upload/$',						'eav_upload'),
)
