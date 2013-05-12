# -*- coding: utf-8 -*-
'''
lansite.gw.contact.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.address.views',
	
	(r'^contact/(?P<contact_id>\d+)/address_edt/$',									'contact_address_edit'),
	(r'^contact/(?P<contact_id>\d+)/address_add/$',									'contact_address_add'),
	(r'^contact/(?P<contact_id>\d+)/(?P<address_id>\d+)/address_delete/$',			'contact_address_delete'),
	(r'^contact/(?P<contact_id>\d+)/address_save/$',								'contact_address_save'),
		
	(r'^address/getaddress/(?P<parent_id>\d+)/(?P<type_id>\d+)/$',					'address_getaddress'),
	(r'^address/gettype/(?P<parent_id>\d+)/$',										'address_gettype'),
	(r'^address/getalltypes/$',														'address_getalltypes'),
	(r'^address/getcountry/$',														'address_getcountry'),	
	(r'^address/getzip/(?P<address_id>\d+)/$',										'address_getzip'),	
)
