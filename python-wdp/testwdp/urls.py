from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^(?P<path>.*)$',			views.index, name='index'),
)
#print "urls loaded"