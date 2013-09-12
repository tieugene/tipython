# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.conf import settings

def	index(request):
	return redirect('az.views.ripe_list')

def	about(request):
	return direct_to_template(request, 'about.html')

def	common_context(context):
	return {
		'LOGIN_URL' : settings.LOGIN_URL,
	}
