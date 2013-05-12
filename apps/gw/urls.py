# -*- coding: utf-8 -*-
'''
lansite.gw.urls.py
'''

from django.conf.urls.defaults import *
#from django.conf import settings
#import django.views.static
#from django.contrib.auth.views import login, logout
#import django.views.generic
#from models import *

urlpatterns = patterns('gw.views',
	(r'^$',		'index'),
	(r'^',		include('gw.bits.urls')),
	(r'^',		include('gw.contact.urls')),
#	(r'^',		include('gw.task.urls')),
	(r'^',		include('gw.file.urls')),
	(r'^',		include('gw.tagged.urls')),
	(r'^',		include('gw.address.urls')),	

# WordCombination
    (r'^wordcombination/list$',                                                 'wordcombination_list'),
    (r'^wordcombination/edit/(?P<wordcombination_id>\d+)$',                     'wordcombination_edit'),
    (r'^wordcombination/add$',                                                  'wordcombination_add'),
    (r'^wordcombination/delete/(?P<wordcombination_id>\d+)$',                   'wordcombination_delete'),

    (r'^permission/list/$',                                                     'permission_list'),
    (r'^permission/add/(?P<contenttype_id>\d+)$',                               'permission_add'),
    (r'^permission/gettable/(?P<number>\d+)$',                                  'permission_gettable'),
    (r'^permission/save/(?P<contenttype_id>\d+)$',                              'permission_save'),
)
