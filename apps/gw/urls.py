# -*- coding: utf-8 -*-
'''
lansite.gw.urls.py
'''

from django.conf.urls.defaults import *
#from django.conf import settings
#import django.views.static

urlpatterns = patterns('gw.views',
	(r'^$',		'index'),
	(r'^',		include('gw.bits.urls')),
	(r'^',		include('gw.contact.urls')),
	(r'^',		include('gw.task.urls')),
)
