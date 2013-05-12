# -*- coding: utf-8 -*-
'''
lansite.gw.task.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.views',
	(r'^task/list/$',			'task_list'),
	(r'^task/add/$',			'task_add'),
	(r'^task/view/(?P<item_id>\d+)/$',	'task_view'),
	(r'^task/edt/(?P<item_id>\d+)/$',	'task_edit'),
	(r'^task/del/(?P<item_id>\d+)/$',	'task_del'),
	(r'^task/done/(?P<item_id>\d+)/$',	'task_done'),

	(r'^todoc/$',				'todocat_list'),
	(r'^todoc/add/$',			'todocat_add'),
	(r'^todoc/view/(?P<item_id>\d+)/$',	'todocat_view'),
	(r'^todoc/edt/(?P<item_id>\d+)/$',	'todocat_edit'),
	(r'^todoc/del/(?P<item_id>\d+)/$',	'todocat_del'),
	(r'^todoc/addtodo/(?P<item_id>\d+)/$',	'todocat_add_todo'),

	(r'^todo/list/$',			'todo_list'),
	(r'^todo/add/$',			'todo_add'),
	(r'^todo/view/(?P<item_id>\d+)/$',	'todo_view'),
	(r'^todo/edt/(?P<item_id>\d+)/$',	'todo_edit'),
	(r'^todo/del/(?P<item_id>\d+)/$',	'todo_del'),
	(r'^todo/done/(?P<item_id>\d+)/$',	'todo_done'),
#	(r'^todo/addsub/(?P<item_id>\d+)/$',	'todo_addsub'),
#	(r'^todo/onsub/(?P<item_id>\d+)/$',	'todo_onsub'),
#	(r'^todo/unsub/(?P<item_id>\d+)/$',	'todo_unsub'),

	(r'^assignc/list/$',			'assigncat_list'),
	(r'^assignc/add/$',			'assigncat_add'),
	(r'^assignc/view/(?P<item_id>\d+)/$',	'assigncat_view'),
	(r'^assignc/edt/(?P<item_id>\d+)/$',	'assigncat_edit'),
	(r'^assignc/del/(?P<item_id>\d+)/$',	'assigncat_del'),

	(r'^assign/list/$',			'assign_list'),
	(r'^assign/add/$',			'assign_add'),
	(r'^assign/view/(?P<item_id>\d+)/$',	'assign_view'),
	(r'^assign/edt/(?P<item_id>\d+)/$',	'assign_edit'),
	(r'^assign/del/(?P<item_id>\d+)/$',	'assign_del'),
	(r'^assign/route/(?P<item_id>\d+)/$',	'assign_route'),
	(r'^assign/invalid/(?P<item_id>\d+)/$',	'assign_invalid'),
	(r'^assign/duped/(?P<item_id>\d+)/$',	'assign_duped'),
	(r'^assign/accept/(?P<item_id>\d+)/$',	'assign_accept'),
	(r'^assign/done/(?P<item_id>\d+)/$',	'assign_done'),
	(r'^assign/approve/(?P<item_id>\d+)/$',	'assign_approve'),
	(r'^assign/reopen/(?P<item_id>\d+)/$',	'assign_reopen'),
	(r'^assign/mksub/(?P<item_id>\d+)/$',	'assign_mksub'),
	(r'^assign/history/(?P<item_id>\d+)/$',	'assign_history'),
)