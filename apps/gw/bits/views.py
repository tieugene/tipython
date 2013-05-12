# -*- coding: utf-8 -*-
'''
lansite.gw.bits.views.py
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext

# 3. my
from models import *
from forms import *

# 2. other python
import time
from urlparse import urlparse

# 4. siblings
from ref.models import Oksm, KladrShort, Kladr

def	__log_it(request, object, action, change_message=''):
	'''
	Log this activity
	'''
	LogEntry.objects.log_action(
		user_id         = request.user.id,
		content_type_id = ContentType.objects.get_for_model(object).pk,
		object_id       = object.pk, 
		object_repr     = object.asstr(), # Message you want to show in admin action list
		change_message  = u'GW.UI: ' + change_message, # I used same
		action_flag     = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
	)

def	any_idx(request, dir, model):
	'''
	@param dir:str - directory of idx.html
	@param model:Model - model to list
	'''
	#return render_to_response('gw/%s/idx.html' % dir, context_instance=RequestContext(request, {'item_list': model.objects.all()}))
	return render_to_response('gw/%s_index.html' % dir, context_instance=RequestContext(request, {'item_list': model.objects.all()}))

def	any_dtl(request, dir, model, item_id):
	'''
	@param dir:str - directory of dtl.html
	@param model:Model - model to dtl
	'''
	return render_to_response('gw/%s_detail.html' % dir, context_instance=RequestContext(request, {'item': model.objects.get(pk=item_id)}))

def	any_add(request, dir, model, form):
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		f = form(request.POST)
		if f.is_valid():
			f.save()
			return HttpResponseRedirect(next)
	else:	# GET
		f = form()
	return render_to_response('gw/%s_edit.html' % dir, context_instance=RequestContext(request, {'form': f, 'mode': True, 'next': next}))

def	any_edt(request, dir, model, form, item_id):
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	item = model.objects.get(pk=item_id)
	if request.method == 'POST':
		f = form(request.POST, instance=item)
		if f.is_valid():
			f.save()
			return HttpResponseRedirect(next)
	else:	# GET
		f = form(instance=item)
	return render_to_response('gw/%s_edit.html' % (dir), context_instance=RequestContext(request, {'form': f, 'mode': False, 'next': next}))

def	any_del(request, dir, model, item_id):
	model.objects.get(pk=item_id).delete()
	return any_idx(request, dir, model)

def	address_index(request):
	'''
	Select country
	@param item_id:int - contact id
	'''
	next = request.REQUEST.get('next', None)
	#if (next == None):
	#	return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = SelectCountryForm(request.POST)
		if form.is_valid():
			item = form.cleaned_data['item']
			url = reverse('gw.views.address_detail', kwargs={'item_id': item.id})
			if (next):
				url +=  ('?next=' + next)
			return HttpResponseRedirect(url)
	else:	# GET
		form = SelectCountryForm()
	return render_to_response('gw/address_index.html', context_instance=RequestContext(request, {'form': form, 'next': next}))

def	__show_detail(request, item_id, next, formshort):
	item = Address.objects.get(pk=item_id)
	idlist = list(set(item.get_children().values_list('type', flat=True)))
	qunused = AddrShort.objects.exclude(id__in=idlist).order_by('name')
	formaddress = AddressAddForm1(qunused)
	qused = AddrShort.objects.filter(id__in=idlist).order_by('name')
	form = ChoiceForm(qused)
	return render_to_response('gw/address_detail.html', context_instance=RequestContext(request, {
		'item': item,
		'form': form,
		'isused': bool(qused.count()),
		'formaddress': formaddress,
		'isunused': bool(qunused.count()),
		'formshort': formshort,
		'next': next
	}))

def	address_detail(request, item_id):
	'''
	Address details
	@param item_id - Address.id
	'''
	next = request.REQUEST.get('next', None)
	if request.method == 'POST':
		form = ChoiceForm(AddrShort.objects.all(), request.POST)
		if form.is_valid():	# всегда
			short = form.cleaned_data['item']
			url = reverse('gw.views.address_short', kwargs={'item_id': int(item_id), 'short_id': short.id})
			if (next):
				url +=  ('?next=' + next)
			return HttpResponseRedirect(url)
	return __show_detail(request, item_id, next, AddrShortForm())

def	address_add(request, item_id):
	'''
	Add new address
	'''
	next = request.REQUEST.get('next', None)
	item	= Address.objects.get(pk=item_id)
	idlist	= list(set(item.get_children().values_list('type', flat=True)))	# children's shorts
	qunused	= AddrShort.objects.exclude(id__in=idlist).order_by('name')	# unused shorts
	form = AddressAddForm1(qunused, request.POST)
	if form.is_valid():
		new_item = form.save(commit=False)
		new_item.parent = item
		new_item.save()
		form = AddressAddForm1(qunused)
		item = new_item
	qused = AddrShort.objects.filter(id__in=idlist).order_by('name')
	return render_to_response('gw/address_detail.html', context_instance=RequestContext(request, {
		'item': item,
		'form': ChoiceForm(qused),
		'isused': bool(qused.count()),
		'formaddress': form,
		'isunused': bool(qunused.count()),
		'formshort': AddrShortForm(),
		'next': next
	}))

def	address_add_short(request, item_id):
	'''
	Add new AddShort
	@param addr_id - Address.id
	'''
	next = request.REQUEST.get('next', None)
	form = AddrShortForm(request.POST)
	if form.is_valid():
		form.save()
		form = AddrShortForm()
	return __show_detail(request, item_id, next, form)

def	address_edit(request, item_id):
	next = request.REQUEST.get('next', None)
	item = Address.objects.get(pk=item_id)
	if request.method == 'POST':
		form = AddressEditForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save(commit=False)
			if item.endpoint():
				item.mkfullname()
			else:
				item.fullname = None
			item.save()
			url = reverse('gw.views.address_detail', kwargs={'item_id': int(item_id)})
			if (next):
				url +=  ('?next=' + next)
			return HttpResponseRedirect(url)
	else:	# GET
		form = AddressEditForm(instance=item)
	return render_to_response('gw/address_edit.html', context_instance=RequestContext(request, {
		'item':	item,
		'form':	form,
		'next': next
	}))

def	address_del(request, item_id):
	item = Address.objects.get(pk=item_id)
	parent = item.parent
	item.delete()
	return address_short(request, parent.id)

def	address_short(request, item_id, short_id):
	'''
	Select next address w/ predefined short.
	@param item_id - Address.id
	@param short_id - AddrShort.id
	'''
	next = request.REQUEST.get('next', None)
	item = Address.objects.get(pk=item_id)
	short = AddrShort.objects.get(pk=short_id)
	q = item.get_children().filter(type=short).order_by('name')
	if request.method == 'POST':
		form = ChoiceForm(q, request.POST)
		if form.is_valid():
			item = form.cleaned_data['item']
			url = reverse('gw.views.address_detail', kwargs={'item_id': item.id})
			if (next):
				url +=  ('?next=' + next)
			return HttpResponseRedirect(url)
	return render_to_response('gw/address_short.html', context_instance=RequestContext(request, {
		'item': item,
		'short': short,
		'form': ChoiceForm(q),
		'formadd': AddressAddForm2(),
		'next': next
	}))

def	address_short_add(request, item_id, short_id):
	'''
	Add new address w/ predefined short
	@param item_id - Address.id
	@param short_id - AddrShort.id
	'''
	next = request.REQUEST.get('next', None)
	item = Address.objects.get(pk=item_id)
	short = AddrShort.objects.get(pk=short_id)
	if request.method == 'POST':
		formadd = AddressAddForm2(request.POST)
		if formadd.is_valid():
			new_item = formadd.save(commit=False)
			new_item.parent = item
			new_item.type = short
			new_item.mkfullname()
			new_item.save()
			url = reverse('gw.views.address_detail', kwargs={'item_id': new_item.id})
			if (next):
				url +=  ('?next=' + next)
			return HttpResponseRedirect(url)
	q = item.get_children().filter(type=short).order_by('name')
	return render_to_response('gw/address_short.html', context_instance=RequestContext(request, {
		'item': item,
		'short': short,
		'form': ChoiceForm(q),
		'formadd': formadd,
		'next': next
	}))

def	__addr_recuring(addrshort, k0, a0):
	'''
	recuring add address from Kladr to Address
	'''
	for k in (k0.get_children()):
		__addr_recuring(addrshort, k, Address.objects.create(parent=a0, name=k.name, type=addrshort[k.short.id-1], publish=True, zip=k.zip, fullname = a0.name + ", " + k.name))

@transaction.commit_on_success
def	address_init(request):
	'''
	Init Addressess from OKSM and KLADR
	'''
	t = time.time()
	#print "START:"
	Address.objects.all().delete()
	AddrShort.objects.all().delete()
	AddrKladr.objects.all().delete()
	addrshort = list()
	#1. fill AddrShort
	#print "AddrShort...:", int(time.time() - t)
	for i in KladrShort.objects.order_by('id'):
		addrshort.append(AddrShort.objects.create(id=i.id, name=i.name, fullname=i.fullname))
	#2. Add OKSM
	#print "OKSM...:", int(time.time() - t)
	for i in Oksm.objects.all():
		country = Address.objects.create(name=i.name, publish=True, fullname=i.name)
		if i.id == 643:
			ru = country
	#3. recuring add KLADR (+AddrKladdr)
	#print "Inserting...:", int(time.time() - t)
	cnt = 0
	for k in (Kladr.objects.all().order_by('id')):
		if k.parent:
			#parent = AddrKladr.objects.get(kladr=k.parent).address - 10k/240s
			parent = parents[k.parent.id]
		else:
			parent = ru
			parents = dict()
		address = Address.objects.create(parent=parent, name=k.name, type=addrshort[k.short.id-1], publish=True, zip=k.zip, fullname = ru.name + ", " + k.name)
		AddrKladr.objects.create(kladr = k, address = address)
		parents[k.id] = address
		cnt += 1
		if cnt > 100000:
			break
	#print "END:", int(time.time() - t)
	return HttpResponseRedirect(reverse('gw.views.address_index'))

def	phone_index(request):
	return any_idx(request, 'phone', Phone)

def	phone_detail(request, item_id):
	return any_dtl(request, 'phone', Phone, item_id)

def	phone_add(request):
	return any_add(request, 'phone', Phone, PhoneForm)

def	phone_edit(request, item_id):
	return any_edt(request, 'phone', Phone, PhoneForm, item_id)

def	phone_del(request, item_id):
	return any_del(request, 'phone', Phone, item_id)

def	www_index(request):
	return any_idx(request, 'www', WWW)

def	www_detail(request, item_id):
	return any_dtl(request, 'www', WWW, item_id)

def	www_add(request):
	return any_add(request, 'www', WWW, WWWForm)

def	www_edit(request, item_id):
	return any_edt(request, 'www', WWW, WWWForm, item_id)

def	www_del(request, item_id):
	return any_del(request, 'www', WWW, item_id)

def	email_index(request):
	return any_idx(request, 'email', Email)

def	email_detail(request, item_id):
	return any_dtl(request, 'email', Email, item_id)

def	email_add(request):
	return any_add(request, 'email', Email, EmailForm)

def	email_edit(request, item_id):
	return any_edt(request, 'email', Email, EmailForm, item_id)

def	email_del(request, item_id):
	return any_del(request, 'email', Email, item_id)

def	im_index(request):
	return any_idx(request, 'im', IM)

def	im_detail(request, item_id):
	return any_dtl(request, 'im', IM, item_id)

def	im_add(request):
	return any_add(request, 'im', IM, IMForm)

def	im_edit(request, item_id):
	return any_edt(request, 'im', IM, IMForm, item_id)

def	im_del(request, item_id):
	return any_del(request, 'im', IM, item_id)
