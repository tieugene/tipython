# -*- coding: utf-8 -*-
'''
lansite.apps.contact.url
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('apps.contact.views',
	(r'^$',						'index'),

	(r'^contact/(?P<object_id>\d+)/$',		'contact_detail'),
	(r'^contact/(?P<object_id>\d+)/edit/$',		'contact_edit'),
	(r'^contact/(?P<object_id>\d+)/del/$',		'contact_del'),
	
	(r'^contact/(?P<object_id>\d+)/addr_edt/$',	'contact_addr_edit'),
	(r'^contact/(?P<object_id>\d+)/addr_del/$',	'contact_addr_del'),
	(r'^contact/(?P<object_id>\d+)/addr_add/$',	'contact_addr_add'),
		
	(r'^contact/(?P<object_id>\d+)/phone_add/$',	'contact_phone_add'),
	(r'^contact/(?P<object_id>\d+)/phone_edt/$',	'contact_phone_edit'),
	(r'^contact/(?P<object_id>\d+)/phone_del/$',	'contact_phone_del'),
	(r'^contact/(?P<object_id>\d+)/www_add/$',	'contact_www_add'),
	(r'^contact/(?P<object_id>\d+)/www_edt/$',	'contact_www_edit'),
	(r'^contact/(?P<object_id>\d+)/www_del/$',	'contact_www_del'),
	(r'^contact/(?P<object_id>\d+)/email_add/$',	'contact_email_add'),
	(r'^contact/(?P<object_id>\d+)/email_edt/$',	'contact_email_edit'),
	(r'^contact/(?P<object_id>\d+)/email_del/$',	'contact_email_del'),
	(r'^contact/(?P<object_id>\d+)/im_add/$',	'contact_im_add'),
	(r'^contact/(?P<object_id>\d+)/im_edt/$',	'contact_im_edit'),
	(r'^contact/(?P<object_id>\d+)/im_del/$',	'contact_im_del'),

	(r'^org/$',					'org_index'),
	(r'^org/setabc/(?P<abc>\d+)/$',			'org_setabc'),
	(r'^org/add/$',					'org_add'),
	(r'^org/(?P<object_id>\d+)/$',			'org_detail'),
	(r'^org/(?P<object_id>\d+)/edit/$',		'org_edit'),
	(r'^org/(?P<object_id>\d+)/del/$',		'org_del'),
	(r'^org/(?P<object_id>\d+)/stuff/add/$',	'org_stuff_add'),
	(r'^org/(?P<object_id>\d+)/stuff/edit/$',	'org_stuff_edit'),
	(r'^org/(?P<object_id>\d+)/stuff/del/$',	'org_stuff_del'),

	(r'^person/$',					'person_index'),
	(r'^person/setabc/(?P<abc>\d+)/$',		'person_setabc'),
	(r'^person/add/$',				'person_add'),
	(r'^person/(?P<object_id>\d+)/$',		'person_detail'),
	(r'^person/(?P<object_id>\d+)/edit/$',		'person_edit'),
	(r'^person/(?P<object_id>\d+)/del/$',		'person_del'),
	(r'^person/(?P<object_id>\d+)/stuff/add/$',	'person_stuff_add'),
	(r'^person/(?P<object_id>\d+)/stuff/del/$',	'person_stuff_del'),
	(r'^person/(?P<object_id>\d+)/stuff/edit/$',	'person_stuff_edit'),
	(r'^person/vcard_export/$',			'person_vcard_export'),
	(r'^person/vcard_import/$',			'person_vcard_import'),
	(r'^person/dav/',				'dav'),

	(r'^jobrole/$',					'jobrole_index'),
	(r'^jobrole/setabc/(?P<abc>\d+)/$',		'jobrole_setabc'),
	(r'^jobrole/add/$',				'jobrole_add'),
	(r'^jobrole/(?P<object_id>\d+)/$',		'jobrole_detail'),
	(r'^jobrole/(?P<object_id>\d+)/edit/$',		'jobrole_edit'),
	(r'^jobrole/(?P<object_id>\d+)/del/$',		'jobrole_del'),	
)
