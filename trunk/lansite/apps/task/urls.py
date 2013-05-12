# -*- coding: utf-8 -*-
'''
lansite.apps.task.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('apps.task.views',
	(r'^$',						'index'),
	(r'^task/all/$',				'task_index_all'),
	(r'^task/(?P<object_id>\d+)/$',			'task_detail'),
	(r'^task/(?P<object_id>\d+)/edit/$',		'task_edit'),
	(r'^task/(?P<object_id>\d+)/del/$',		'task_del'),

	(r'^category/$',				'category_index'),
	(r'^category/add/$',				'category_add'),
	(r'^category/(?P<object_id>\d+)/$',		'category_detail'),
	(r'^category/(?P<object_id>\d+)/edit/$',	'category_edit'),
	(r'^category/(?P<object_id>\d+)/del/$',		'category_del'),
	(r'^category/(?P<object_id>\d+)/addtodo/$',	'category_add_todo'),

	(r'^ical/$',					'ical_index'),

	(r'^todo/$',					'todo_index'),
	(r'^todo/set_columns/$',			'todo_index_setcolumns'),
	(r'^todo/set_sort/$',				'todo_index_setsort'),
	(r'^todo/set_filter/$',				'todo_index_setfilter'),
	(r'^todo/add/$',				'todo_add'),
	(r'^todo/del_selected/$',			'todo_del_selected'),
	(r'^todo/(?P<object_id>\d+)/$',			'todo_detail'),
	(r'^todo/(?P<object_id>\d+)/(?P<cols>\d+)/$',	'todo_detail_setcols'),
	(r'^todo/(?P<object_id>\d+)/links/$',		'todo_links'),
	(r'^todo/(?P<object_id>\d+)/perm_view/$',	'todo_perm_view'),
	(r'^todo/(?P<object_id>\d+)/perm_setg/$',	'todo_perm_setg'),
	(r'^todo/(?P<object_id>\d+)/perm_delg/$',	'todo_perm_delg'),
	(r'^todo/(?P<object_id>\d+)/perm_setu/$',	'todo_perm_setu'),
	(r'^todo/(?P<object_id>\d+)/perm_delu/$',	'todo_perm_delu'),
	(r'^todo/(?P<object_id>\d+)/log/$',		'todo_log'),
	(r'^todo/(?P<object_id>\d+)/tags/$',		'todo_tags'),
	(r'^todo/(?P<object_id>\d+)/edit/$',		'todo_edit'),
	(r'^todo/(?P<object_id>\d+)/del/$',		'todo_del'),
	(r'^todo/(?P<object_id>\d+)/done/$',		'todo_done'),
	(r'^todo/(?P<object_id>\d+)/addcat/$',		'todo_addcat'),
	(r'^todo/(?P<object_id>\d+)/delcat/$',		'todo_delcat'),
	(r'^todo/(?P<object_id>\d+)/sub_add/$',		'todo_sub_add'),
	(r'^todo/sub_del/(?P<object_id>\d+)/$',		'todo_sub_del'),
	(r'^todo/ical_export/$',			'todo_ical_export'),
	(r'^todo/ical_import/$',			'todo_ical_import'),
	(r'^todo/ical_export2/$',			'todo_ical_export2'),
	(r'^todo/ical_import2/$',			'todo_ical_import2'),

	(r'^todo/cat/add/$',				'todo_cat_add'),
	(r'^todo/cat/(?P<object_id>\d+)/edit/$',	'todo_cat_edit'),
	(r'^todo/cat/(?P<object_id>\d+)/del/$',		'todo_cat_del'),
	(r'^todo/cat/del_selected/$',			'todo_cat_del_selected'),
)
