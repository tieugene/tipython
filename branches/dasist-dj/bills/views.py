# -*- coding: utf-8 -*-

# 1. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.utils.datastructures import SortedDict

# 2. system
import os, imp, pprint

# 3. 3rd party

# 4. my
#import forms, models
import models

PAGE_SIZE = 20

@login_required
def	bill_list(request):
	'''
	List of bills
	ACL: assign|approve=user
	'''
	#tpl = moduledict[uuid]
	#if request.user.is_authenticated():
	#	queryset = models.Doc.objects.filter(user=request.user, type=uuid).order_by('name')
	#else:
	#	queryset = models.Doc.objects.none()
	queryset = models.Bill.objects.all()
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'bills/list.html',
	)

@login_required
def	bill_add(request):
	'''
	Anonymous form
	'''
	return __doc_acu(request, uuid, 0)

@login_required
def	bill_view(request, id):
	'''
	Read (view) document
	'''
	return __doc_rvp(request, id, 0)

@login_required
def	bill_edit(request, id):
	'''
	Update (edit) document
	'''
	return __doc_acu(request, id, 2)

@login_required
def	bill_accept(request, id):
	'''
	Preview document
	'''
	return __doc_rvp(request, id, 1)

@login_required
def	bill_reject(request, id):
	'''
	Print document
	'''
	return __doc_rvp(request, id, 2)
