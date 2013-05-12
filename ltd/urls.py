# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	#staticfiles_urlpatterns(),
	#url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
	url(r'^$',				'views.index'),
	url(r'^about$',				'views.about'),
	url(r'^doctype/$',			'views.doctype_index'),
	url(r'^doctype/(?P<item_id>\d+)/$',	'views.doctype_detail'),
	url(r'^doc/(?P<item_id>\d+)/add/$',	'views.doc_add'),
	url(r'^doc/(?P<item_id>\d+)/$',		'views.doc_detail'),
	url(r'^doc/(?P<item_id>\d+)/edit/$',	'views.doc_edit'),
	url(r'^doc/(?P<item_id>\d+)/del/$',	'views.doc_del'),
)
