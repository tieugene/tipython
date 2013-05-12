# -*- coding: utf-8 -*-
'''
lansite.gw.task.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.tagged.views',
	(r'^to/list/$',				'to_list'),
	(r'^to/add/$',				'to_add'),
    (r'^to/search/$',				'to_search'),
    (r'^to/add/(?P<obj_id>\d+)/(?P<type_id>\d+)$',			'to_add_instant'),
    (r'^to/add/tagtype$',				'to_tagtype_add'),
    (r'^to/add/objtype$',				'to_objtype_add'),
	(r'^to/view/(?P<item_id>\d+)/$',	'to_view'),
    (r'^to/attach/(?P<item_id>\d+)/$',	'to_attach'),
	(r'^to/edit/(?P<item_id>\d+)/$',	'to_edit'),
    (r'^to/edit/(?P<item_id>\d+)/newtag$',	'to_edit_newtag'),
    (r'^to/edit/(?P<item_id>\d+)/deltag/(?P<tag_id>\d+)$',	'to_edit_deltag'),
    (r'^to/deltagtype/(?P<tagtype_id>\d+)$',	'to_deltagtype'),
	(r'^to/del/(?P<item_id>\d+)/$',		'to_del'),
    (r'^to/getinput/(?P<item_id>\d+)/$',		'to_get_input'),
    (r'^to/ctype/$',				'ctype'),
    (r'^to/upload/$',				'uploadTOTs'),
)
