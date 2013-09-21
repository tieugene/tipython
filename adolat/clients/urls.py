# -*- coding: UTF-8 -*-
__author__ = 'sdv'


from django.conf.urls.defaults import *
from clients import views
#from clients.views import ClientDetailView,ClientFormView,ClientListView


urlpatterns = patterns('clients.views',
    url(r'^$', views.index),
    url(r'^add/$', views.add),
    url(r'^(?P<client_id>\d+)/$', views.detail),
    url(r'^(?P<client_id>\d+)/edit/$', views.edit),
    url(r'^(?P<client_id>\d+)/updated/$', views.updated),
    url(r'^(?P<client_id>\d+)/remove/$', views.remove),
    #url(r'^$', ClientListView.as_view(), name='index')
)
