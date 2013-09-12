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
import os, sys, pprint

# 3. 3rd party

# 4. my
import forms, models

PAGE_SIZE = 20

def	ripe_list(request):
	'''
	List of RIPE records
	'''
	#return render_to_response('ripe_list.html', context_instance=RequestContext(request))
	#return render_to_response('ripe_list.html', context_instance=RequestContext(request, {'data': moduledict,}))
        return  object_list (
                request,
                queryset = models.RIPE.objects.all(),
                paginate_by = PAGE_SIZE,
                page = int(request.GET.get('page', '1')),
                template_name = 'ripe_list.html',
        )

def	ripe_detail(request, id):
        return  object_detail (
                request,
                queryset = models.RIPE.objects.all(),
                object_id = id,
                template_name = 'ripe_detail.html', # FIXME:
        )
