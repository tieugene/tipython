# -*- coding: utf-8 -*-
'''
lansite.gw.bits.urls.py
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('gw.bits.views',
	(r'^bits/$',							'bits_index'),

	(r'^address/$',							'address_index'),
	(r'^address/init/$',						'address_init'),
	(r'^address/(?P<item_id>\d+)/$',				'address_detail'),
	(r'^address/(?P<item_id>\d+)/edit/$',				'address_edit'),
	(r'^address/(?P<item_id>\d+)/del/$',				'address_del'),
	(r'^address/(?P<item_id>\d+)/add/$',				'address_add'),
	(r'^address/(?P<item_id>\d+)/add_short/$',			'address_add_short'),
	(r'^address/(?P<item_id>\d+)/short/(?P<short_id>\d+)/$',	'address_short'),
	(r'^address/(?P<item_id>\d+)/short/(?P<short_id>\d+)/add/$',	'address_short_add'),

	(r'^phone/$',							'phone_index'),
	(r'^phone/add/$',						'phone_add'),
	(r'^phone/(?P<item_id>\d+)/$',					'phone_detail'),
	(r'^phone/(?P<item_id>\d+)/edit/$',				'phone_edit'),
	(r'^phone/(?P<item_id>\d+)/del/$',				'phone_del'),

	(r'^www/$',							'www_index'),
	(r'^www/add/$',							'www_add'),
	(r'^www/(?P<item_id>\d+)/$',					'www_detail'),
	(r'^www/(?P<item_id>\d+)/edit/$',				'www_edit'),
	(r'^www/(?P<item_id>\d+)/del/$',				'www_del'),

	(r'^email/$',							'email_index'),
	(r'^email/add/$',						'email_add'),
	(r'^email/(?P<item_id>\d+)/$',					'email_detail'),
	(r'^email/(?P<item_id>\d+)/edit/$',				'email_edit'),
	(r'^email/(?P<item_id>\d+)/del/$',				'email_del'),

	(r'^im/$',							'im_index'),
	(r'^im/add/$',							'im_add'),
	(r'^im/(?P<item_id>\d+)/$',					'im_detail'),
	(r'^im/(?P<item_id>\d+)/edit/$',				'im_edit'),
	(r'^im/(?P<item_id>\d+)/del/$',					'im_del'),
)
