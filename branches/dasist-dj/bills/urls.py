# -*- coding: utf-8 -*-
'''
lansite.apps.core.urls
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('bills.views',
	url(r'^$',			'bill_list'),	# GET; ACL: assign|approve=user
	url(r'^a/$',			'bill_add'),	# GET/POST; ACL: assign, Cancel > list; save > view (Draft)
	url(r'^(?P<id>\d+)/$',		'bill_view'),	# GET; ACL: assign|approv
	url(r'^(?P<id>\d+)/u/$',	'bill_edit'),	# GET/POST; ACL: assign+draft;
	url(r'^(?P<id>\d+)/y/$',	'bill_accept'),	# POST; ACL: approve;
	url(r'^(?P<id>\d+)/n/$',	'bill_reject'),	# POST; ACL: approve;
	url(r'^(?P<id>\d+)/d/$',	'bill_delete'),	# GET; ACL: assign;
)
