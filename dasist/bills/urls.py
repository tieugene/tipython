# -*- coding: utf-8 -*-
'''
lansite.apps.core.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('bills.views',
	url(r'^$',			'bill_list'),	# GET; ACL: assign|approve=user
	url(r'^lpp/(?P<lpp>\d+)/$',	'bill_set_lpp'),
	url(r'^mode/(?P<mode>\d+)/$',	'bill_set_mode'),
	url(r'^fs/$',			'bill_filter_state'),
	url(r'^a/$',			'bill_add'),	# GET/POST; ACL: assign, Cancel > list; save > view (Draft)
	url(r'^(?P<id>\d+)/$',		'bill_view'),	# GET; ACL: assign|approv
	url(r'^(?P<id>\d+)/u/$',	'bill_edit'),	# GET/POST; ACL: assign+draft;
	url(r'^(?P<id>\d+)/ru/$',	'bill_reedit'),	# GET/POST; ACL: assign+draft?;
	url(r'^(?P<id>\d+)/d/$',	'bill_delete'),	# GET; ACL: assign;
	url(r'^(?P<id>\d+)/s/$',	'bill_toscan'),
	url(r'^(?P<id>\d+)/r/$',	'bill_restart'),
	url(r'^(?P<id>\d+)/mail/$',	'mailto'),
#	url(r'^(?P<id>\d+)/g/$',	'bill_get'),	# GET; ACL: assign;
)
