# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from django.conf.urls import patterns, url
from reception import views


urlpatterns = patterns('reception.views',
    url(r'^$', views.index),
)
