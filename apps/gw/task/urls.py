# -*- coding: utf-8 -*-
'''
lansite.gw.task.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.task.views',
	(r'^task/$',					'task_index'),
	(r'^task/all/$',				'task_index_all'),
	(r'^task/(?P<item_id>\d+)/$',			'task_detail'),
	(r'^task/(?P<item_id>\d+)/edit/$',		'task_edit'),
	(r'^task/(?P<item_id>\d+)/del/$',		'task_del'),

	(r'^category/$',				'category_index'),
	(r'^category/add/$',				'category_add'),
	(r'^category/(?P<item_id>\d+)/$',		'category_detail'),
	(r'^category/(?P<item_id>\d+)/edit/$',		'category_edit'),
	(r'^category/(?P<item_id>\d+)/del/$',		'category_del'),
	(r'^category/(?P<item_id>\d+)/addtodo/$',	'category_add_todo'),

	(r'^ical/$',					'ical_index'),

	(r'^todo/$',					'todo_index'),
	(r'^todo/set_columns/$',			'todo_index_setcolumns'),
	(r'^todo/set_sort/$',				'todo_index_setsort'),
	(r'^todo/set_filter/$',				'todo_index_setfilter'),
	(r'^todo/add/$',				'todo_add'),
	(r'^todo/(?P<item_id>\d+)/$',			'todo_detail'),
	(r'^todo/(?P<item_id>\d+)/edit/$',		'todo_edit'),
	(r'^todo/(?P<item_id>\d+)/del/$',		'todo_del'),
	(r'^todo/(?P<item_id>\d+)/done/$',		'todo_done'),
	(r'^todo/(?P<item_id>\d+)/addcat/$',		'todo_addcat'),
	(r'^todo/(?P<item_id>\d+)/delcat/$',		'todo_delcat'),
	(r'^todo/cat/add/$',				'todo_cat_add'),
	(r'^todo/cat/(?P<item_id>\d+)/edit/$',		'todo_cat_edit'),
	(r'^todo/cat/(?P<item_id>\d+)/del/$',		'todo_cat_del'),
	(r'^todo/ical_export/$',			'todo_ical_export'),
	(r'^todo/ical_import/$',			'todo_ical_import'),
	(r'^todo/del_selected/$',			'todo_del_selected'),
	(r'^todo/cat/del_selected/$',			'todo_cat_del_selected'),

	(r'^event/$',					'event_index'),
	(r'^event/add/$',				'event_add'),
	(r'^event/(?P<item_id>\d+)/$',			'event_detail'),
	(r'^event/(?P<item_id>\d+)/edit/$',		'event_edit'),
	(r'^event/(?P<item_id>\d+)/del/$',		'event_del'),
)

'''
	(r'^todo/route/(?P<item_id>\d+)/$',		'todo_route'),
	(r'^todo/accept/(?P<item_id>\d+)/$',		'todo_accept'),
	(r'^todo/approve/(?P<item_id>\d+)/$',		'todo_approve'),
	(r'^todo/reopen/(?P<item_id>\d+)/$',		'todo_reopen'),
	(r'^todo/mksub/(?P<item_id>\d+)/$',		'todo_mksub'),
	(r'^todo/history/(?P<item_id>\d+)/$',		'todo_history'),

'''
