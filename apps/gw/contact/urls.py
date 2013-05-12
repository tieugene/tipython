# -*- coding: utf-8 -*-
'''
lansite.gw.contact.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.contact.views',
	(r'^contact/$',							'contact_index'),
	(r'^contact/all/$',						'contact_index_all'),
	(r'^contact/add/$',						'contact_add'),
	(r'^contact/(?P<item_id>\d+)/$',				'contact_detail'),
	(r'^contact/(?P<item_id>\d+)/edit/$',				'contact_edit'),
	(r'^contact/(?P<item_id>\d+)/del/$',				'contact_del'),
	
	(r'^contact/(?P<item_id>\d+)/addr_edt/$',			'contact_addr_edit'),
	(r'^contact/(?P<item_id>\d+)/addr_del/$',			'contact_addr_del'),
	(r'^contact/(?P<item_id>\d+)/addr_add/$',			'contact_addr_add'),
		
	(r'^contact/(?P<item_id>\d+)/phone_add/$',			'contact_phone_add'),
	(r'^contact/(?P<item_id>\d+)/phone_edt/$',			'contact_phone_edit'),
	(r'^contact/(?P<item_id>\d+)/phone_del/$',			'contact_phone_del'),
	(r'^contact/(?P<item_id>\d+)/www_add/$',			'contact_www_add'),
	(r'^contact/(?P<item_id>\d+)/www_edt/$',			'contact_www_edit'),
	(r'^contact/(?P<item_id>\d+)/www_del/$',			'contact_www_del'),
	(r'^contact/(?P<item_id>\d+)/email_add/$',			'contact_email_add'),
	(r'^contact/(?P<item_id>\d+)/email_edt/$',			'contact_email_edit'),
	(r'^contact/(?P<item_id>\d+)/email_del/$',			'contact_email_del'),
	(r'^contact/(?P<item_id>\d+)/im_add/$',				'contact_im_add'),
	(r'^contact/(?P<item_id>\d+)/im_edt/$',				'contact_im_edit'),
	(r'^contact/(?P<item_id>\d+)/im_del/$',				'contact_im_del'),

	(r'^org/$',							'org_index'),
	(r'^org/add/$',							'org_add'),
	(r'^org/(?P<item_id>\d+)/$',					'org_detail'),
	(r'^org/(?P<item_id>\d+)/edit/$',				'org_edit'),
	(r'^org/(?P<item_id>\d+)/del/$',				'org_del'),
	(r'^org/(?P<item_id>\d+)/stuff/add/$',				'org_stuff_add'),
	(r'^org/(?P<item_id>\d+)/stuff/edit/$',				'org_stuff_edit'),
	(r'^org/(?P<item_id>\d+)/stuff/del/$',				'org_stuff_del'),

	(r'^person/$',							'person_index'),
	(r'^person/add/$',						'person_add'),
	(r'^person/(?P<item_id>\d+)/$',					'person_detail'),
	(r'^person/(?P<item_id>\d+)/edit/$',				'person_edit'),
	(r'^person/(?P<item_id>\d+)/del/$',				'person_del'),
	(r'^person/(?P<item_id>\d+)/stuff/add/$',			'person_stuff_add'),
	(r'^person/(?P<item_id>\d+)/stuff/del/$',			'person_stuff_del'),
	(r'^person/(?P<item_id>\d+)/stuff/edit/$',			'person_stuff_edit'),

	(r'^role/$',							'role_index'),
	(r'^role/add/$',						'role_add'),
	(r'^role/(?P<item_id>\d+)/$',				'role_detail'),
	(r'^role/(?P<item_id>\d+)/edit/$',				'role_edit'),
	(r'^role/(?P<item_id>\d+)/del/$',				'role_del'),
)
