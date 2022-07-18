# -*- coding: utf-8 -*-
'''
views.py

index (client list w/ A-Z, today, calendar; settings - in cookie)
client: CRUD + img CRD + search on F/phone + sort on date
record: LCRUD (in client or calendar)
'''

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext, Context, loader
#from django.views.generic import ListView, DetailView
from django.http import HttpResponse

import datetime, collections, os, urllib
from mimetypes import MimeTypes
mime = MimeTypes()

import models, forms

LPP = 25
ABC = u'*АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ'
CAL = collections.OrderedDict()
for i in xrange(15):
	for j in xrange(2):
		CAL['%02d:%02d' % (i + 8, j * 30)] = i * 2 + j

def	__get_end_time(t0, d):
	'''
	@param t:time - start time
	@param d:int - duration (in 30')
	@return - end time - 1"
	TODO: свернуть
	'''
	secs0 = t0.hour * 3600 + t0.minute * 60
	secsd = (d+1) * 1800 - 1
	secs1 = secs0 + secsd
	hours1 = secs1 // 3600
	mins1 = (secs1-(hours1*3600)) // 60
	t1 = datetime.time(hours1, mins1, 59)
	return t1

def	index(request):
	#del request.session['date']
	# 1. session filters/sorts defaults: client.abc, client.sort, client.page, record.date
	if 'abc' not in request.session:
		request.session['abc'] = 0	# *
	if 'sort' not in request.session:
		request.session['sort'] = 1	# 1-2: id (v-^), 3-4: lname>fname>mname; 5-6: date
	if 'page' not in request.session:
		request.session['page'] = 1
	if 'date' not in request.session:
		request.session['date'] = datetime.date.today().isoformat()
	# 2. go
	# 2.1. clients
	# 2.1.1. filter/sort clients
	clients = models.Client.objects.all()
	abc = request.session['abc']
	if abc:
		clients = clients.filter(lname__startswith=ABC[abc])
	sort = int(request.session['sort'])
	if sort == 1:
		clients = clients.order_by('pk')
	elif sort == 2:
		clients = clients.order_by('-pk')
	elif sort == 3:
		clients = clients.order_by('lname')
	elif sort == 4:
		clients = clients.order_by('-lname')
	# 2.1.2. paging
	paginator = Paginator(clients, LPP)
	page = int(request.GET.get('page', 1))
	try:
		clients = paginator.page(page)
	except PageNotAnInteger:
		clients = paginator.page(1)			# page is not an integer, deliver first page.
	except EmptyPage:
		clients = paginator.page(paginator.num_pages)	# page is out of range (e.g. 9999), deliver last page of results.
	# 2.2. records
	date = datetime.datetime.strptime(request.session['date'], '%Y-%m-%d').date()
	records = models.Record.objects.filter(date=date)
	cal = CAL.keys()
	for rec in records:
		hhmm = rec.time.strftime('%H:%M')
		i = CAL[hhmm]
		cal[i] = (hhmm, rec)
		for j in xrange(rec.durat):	# fill unusable
			if (i+j) < len(cal):
				cal[i+j+1] = (cal[i+j+1], None)
	for i in xrange(len(cal)):		# fill empty
		if len(cal[i]) != 2:
			cal[i] = (cal[i], 0)
	# 3. result
	return render_to_response('index.html', context_instance=RequestContext(request, {
                'clients': clients,
		#'records': records,
		'records': cal,
		'form': forms.FilterForm(initial={'date': date}),
        }))

# = Client =
def	client_view(request, pk):
	object = get_object_or_404(models.Client, pk=int(pk))
	if request.method == 'POST':	# uploading file
		form = forms.FileForm(request.POST, request.FILES)
		if form.is_valid():
			object.img_add(request.FILES['file'])
	else:
		form = forms.FileForm()
	return render_to_response('client_detail.html', context_instance=RequestContext(request, {
		'object': object,
		'prev': models.Client.objects.filter(pk__lt = object.pk).order_by('-pk').first(),
		'next': models.Client.objects.filter(pk__gt = object.pk).order_by('pk').first(),
		'form': form
        }))

def	client_add(request):
	if request.method == 'POST':
		form = forms.ClientForm(request.POST)
		if form.is_valid():
			object = form.save()
			return redirect('medrec.views.client_view', object.pk)
	else:
		form = forms.ClientForm()
	return render_to_response('client_form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': None,
	}))

def	client_edit(request, pk):
	object = models.Client.objects.get(pk=int(pk))
	if request.method == 'POST':
		form = forms.ClientForm(request.POST, instance=object)
		if form.is_valid():
			object = form.save()
			return redirect('medrec.views.client_view', int(pk))
	else:
		form = forms.ClientForm(instance=object)
	return render_to_response('client_form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': object,
	}))

def	client_del(request, pk):
	'''
	TODO: delete images
	'''
	models.Client.objects.get(pk=int(pk)).delete()
	return redirect('medrec.views.index')

# == set filter/sort ==
def	client_set_filter_abc(request, abc):
	'''
	TODO: range
	'''
	request.session['abc'] = int(abc)
	return redirect('medrec.views.index')

def	client_set_sort(request, sort):
	'''
	TODO: range
	'''
	request.session['sort'] = int(sort)
	return redirect('medrec.views.index')

# = Record =
def	record_view(request, pk):
	object = get_object_or_404(models.Record, pk=int(pk))
	return render_to_response('record_detail.html', context_instance=RequestContext(request, {
		'object': object,
        }))

def	record_add(request):
	if request.method == 'POST':
		form = forms.RecordForm(request.POST)
		if form.is_valid():
			object = form.save()
			return redirect('medrec.views.record_view', object.pk)
	else:
		form = forms.RecordForm()
	return render_to_response('record_form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': None,
	}))

def	record_edit(request, pk):
	pk = int(pk)
	object = models.Record.objects.get(pk=pk)
	msg = ''
	if request.method == 'POST':
		form = forms.RecordForm(request.POST, instance=object)
		if form.is_valid():
			# Don't intercept
			my_beg = form.cleaned_data['time']
			durat = int(form.cleaned_data['durat'])
			my_end = __get_end_time(my_beg, durat)
			for rec in models.Record.objects.filter(date=form.cleaned_data['date']):
				if rec.id != pk:	# let's chk interception
					rec_beg = rec.time
					rec_end = __get_end_time(rec_beg, rec.durat)
					if (rec_beg <= my_end and rec_end >= my_beg):
						msg += '<li> Пересекается с %s (%s) </li>' % (rec, rec.get_durat())
			if (not msg):
				form.save()
				return redirect('medrec.views.record_view', pk)
	else:
		form = forms.RecordForm(instance=object)
	return render_to_response('record_form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': object,
		'msg': msg,
	}))

def	record_del(request, pk):
	models.Record.objects.get(pk=int(pk)).delete()
	return redirect('medrec.views.index')

def	record_set_date(request):
	'''
	TODO: err
	'''
	if request.method == 'POST':
		form = forms.FilterForm(request.POST)
		if form.is_valid():
			request.session['date'] = form.cleaned_data['date'].isoformat()
	return redirect('medrec.views.index')

def	record_get_date(request, date):
	'''
	TODO: err
	'''
	date = datetime.datetime.strptime(date, '%y%m%d').date()
	request.session['date'] = date.isoformat()
	return redirect('medrec.views.index')

# = Image =
def	img_view(request, pk, img):
	object = get_object_or_404(models.Client, pk=int(pk))
	fn = object.get_img_path(img)
	mime_type = mime.guess_type(fn)
	response = HttpResponse(content_type=mime_type[0])
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = '; filename=\"%s\"' % img
	response.write(open(fn).read())
	return response

def	img_del(request, pk, img):
	object = get_object_or_404(models.Client, pk=int(pk))
	object.del_img(img)
	return redirect('medrec.views.client_view', object.pk)
