# -*- coding: utf-8 -*-
'''
Order: beg ASC, end DESC (wider first
Filters:
* top/all (and nothing else)
* IP => 1 record (check reserved IPs: http://en.wikipedia.org/wiki/Reserved_IP_addresses)
* key word => list
* State: not voted/on voting/voted (b/w)
* Findme
TODO:
* top search bar - always
* search IP _or_ word
* word: chk for ascii only
* all == filtered on None
'''

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

# 3. 3rd parties
from iptools import IpRangeList
from iptools.ipv4 import ip2long

# 4. my
import forms, models

PAGE_SIZE = 20

def	__r_list(request, q):
        return  object_list (
                request,
                queryset = q,
                paginate_by = PAGE_SIZE,
                page = int(request.GET.get('page', '1')),
                template_name = 'ripe_list.html',
		extra_context = {
			'ipform': forms.SearchIPForm(),
			'kwform': forms.SearchWordForm(),
		},
        )

def	ripe_list(request):
        return  __r_list (request, models.RIPE.objects.all())

def	ripe_list_top(request):
        return  __r_list (request, models.RIPE.objects.filter(parent__isnull=True))

def	ripe_detail(request, id):
        return  object_detail (
                request,
                queryset = models.RIPE.objects.all(),
                object_id = id,
                template_name = 'ripe_detail.html',
        )

def	search_ip(request):
	if request.method == 'POST':
		form = forms.SearchIPForm(request.POST)
		if form.is_valid():
			ip = ip2long(form.cleaned_data['ip'])
			# beg <= ip AND end >= ip ORDER BY end-beg LIMIT 1
			q = models.RIPE.objects.filter(beg__lte=ip, end__gte=ip).order_by('-beg', 'end')
			if (q.count() > 0):
				return redirect(ripe_detail, id=q[0].pk)
	else:   # GET
		form = SearchIPForm()
	return redirect(ripe_list)

def	search_myip(request):
	'''
	request.META['REMOTE_ADDR']
	'''
	pass

def	search_word(request):
	if request.method == 'POST':
		form = forms.SearchWordForm(request.POST)
		if form.is_valid():
			word = form.cleaned_data['word']
			# beg <= ip AND end >= ip ORDER BY end-beg LIMIT 1
			q = models.RIPEc.objects.filter(v__icontains=word)
			if (q.count() > 0):
				print q.count()
				s = set(q.values_list('ripe__id', flat=True))
				return __r_list (request, models.RIPE.objects.filter(id__in=s))
				# TODO: store form data
				#return redirect(ripe_list)
	else:   # GET
		form = SearchWordForm()
	return redirect(ripe_list)
