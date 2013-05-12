# -*- coding: utf-8 -*-
'''
lansite.apps.contact.views
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext
# generic views
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

# 2. python
import time, datetime, vobject
from urlparse import urlparse

# 3. my
from models import *
from forms import *
from vcard import *
import carddav

# 4. siblings

PAGE_SIZE=20

@login_required
def	index(request):
	return direct_to_template(request, 'contact/index.html')

@login_required
def	contact_detail(request, object_id):
	'''
	FIXME: by get_permalink_url
	'''
	return person_detail(request, object_id) if (Contact.objects.get(pk=object_id).get_real_instance_class() == Person) else org_detail(request, object_id)

@login_required
def	contact_edit(request, object_id):
	return person_edit(request, object_id) if (Contact.objects.get(pk=object_id).get_real_instance_class() == Person) else 	org_edit(request, object_id)

@login_required
def	contact_del(request, object_id):
	#return person_del(request, object_id)
	return person_del(request, object_id) if (Contact.objects.get(pk=object_id).get_real_instance_class() == Person) else org_del(request, object_id)

@login_required
def	contact_addr_edit(request, object_id):
	'''
	Change address of Contact
	@param object_id:int - ContactAddr.id
	@param ?address=<int> - Address to change to
	If address not changed - nothing to do
	If address already exists - delete old
	Else - change to new
	'''
	object = ContactAddr.objects.get(pk=object_id)
	contact = object.contact
	old_address = object.addr
	address_id = request.REQUEST.get('address', None)
	if (address_id):
		new_address = Address.objects.get(pk=address_id)
		if (new_address != old_address):
			if (contact.contactaddr_set.filter(addr=new_address).count()):	# already exists
				object.delete()
			else:
				object.addr = new_address
				object.save()
	return redirect(contact)

@login_required
def	contact_addr_del(request, object_id):
	'''
	Delete address of Contact
	@param object_id:int - ContactAddr.id
	'''
	object = ContactAddr.objects.get(pk=object_id)
	contact = object.contact
	object.delete()
	return redirect(contact)

@login_required
def	contact_addr_add(request, object_id):
	'''
	Add address to contact callback w/ ?address=<selected address id>
	@param object_id - contact id
	@param ?address=<int> - address to add
	'''
	contact = Contact.objects.get(pk=object_id)
	address_id = request.REQUEST.get('address', None)
	if (address_id):
		address = Address.objects.get(pk=address_id)
		object = ContactAddr.objects.create(contact=contact, addr=address)
	return redirect(contact)

@login_required
def	contact_phone_add(request, object_id):
	'''
	Add new Phone to Contact.
	@param object_id - Contact.id
	FIXME: types
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactPhoneForm(request.POST)
		if form.is_valid():
			q = ContactPhone.objects.filter(contact__id=object_id, phone__no=form.cleaned_data['no'])
			if (q.count() == 0):	# realy new; else - do nothing
				ContactPhone(contact=Contact.objects.get(pk=object_id), phone=Phone.objects.get_or_create(no=form.cleaned_data['no'])[0], ext=form.cleaned_data['ext']).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactPhoneForm()
	return render_to_response('core/phone_form.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

@login_required
def	contact_phone_edit(request, object_id):
	'''
	Edit Contact's phone.
	@param object_id:ContactPhone.id
	FIXME: types
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	object = ContactPhone.objects.get(pk=object_id)
	if request.method == 'POST':
		objectlist = list()	# what is it?
		form = ContactPhoneForm(request.POST)
		if form.is_valid():
			no = form.cleaned_data['no']
			# 1. no is not the same
			if (no != object.phone.no):
				oldphone = object.phone
				if (oldphone.contactphone_set.count() == 1):		# такой no есть только у 1 контакта
					if (Phone.objects.filter(no=no).count() == 0):	# новый no не существует в Phone
						oldphone.no = no			# заменит no в Phone
						oldphone.save()
					else:						# новый no существует в Phone
						if (ContactPhone.objects.filter(contact=object.contact, phone__no=no).count() == 0): # не существует для этого контакта
							object.phone = Phone.objects.get(no=no)	# заменить Phone в ContactPhone
							object.save()
						oldphone.delete()				# старый WWW - прибить
				else:							# такой Phone есть только еще у кого-то
					if (Phone.objects.filter(no=no).count() == 0):	# новый no не существует в Phone
						object.phone = Phone.objects.create(no=no)	# создать новый Phone
						object.save()
					else:						# новый no существует в Phone
						if (ContactPhone.objects.filter(contact=object.contact, phone__no=no).count() == 0): # не существует для этого контакта
							object.phone = Phone.objects.get(no=no)	# заменить Phone в ContactPhone
							object.save()
						else:					# существует для этого контакта
							object.delete()			# лишний ContactPhone - прибить
			else:	# no is the same
				ext = form.cleaned_data['ext']
				if (ext != object.ext):
					object.ext = ext
					object.save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactPhoneForm({'no': object.phone.no, 'ext': object.ext})
		objectlist = object.phone.contactphone_set.exclude(pk=object_id)
	return render_to_response('core/phone_form.html', context_instance=RequestContext(request, {'form': form, 'object': object, 'objectlist': objectlist, 'next': next}))

@login_required
def	contact_phone_del(request, object_id):
	'''
	object_id - ContactPhone.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	object = ContactPhone.objects.get(pk=object_id)
	contact = object.contact
	if (object.phone.contactphone_set.count() > 1):
		object.delete()
	else:
		object.phone.delete()
	return HttpResponseRedirect(next)

@login_required
def	contact_www_add(request, object_id):
	'''
	Add new WWW to Contact.
	Check exist and uniq pair contact<>www
	@param object_id - Contact.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactWWWForm(request.POST)
		if form.is_valid():
			if (ContactWWW.objects.filter(contact__id=object_id, www__URL=form.cleaned_data['URL']).count() == 0):	# realy new; else - do nothing
				ContactWWW(contact=Contact.objects.get(pk=object_id), www=WWW.objects.get_or_create(URL=form.cleaned_data['URL'])[0]).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactWWWForm()
	return render_to_response('core/www_form.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

@login_required
def	contact_www_edit(request, object_id):
	'''
	Edit Contact's www.
	@param object_id:ContactWWW.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	object = ContactWWW.objects.get(pk=object_id)
	if request.method == 'POST':
		objectlist = list()
		form = ContactWWWForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['URL']
			# 1. URL is not the same
			if (URL != object.www.URL):
				oldwww = object.www
				if (oldwww.contactwww_set.count() == 1):		# такой WWW есть только у 1 контакта
					if (WWW.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						oldwww.URL = URL			# заменит URL в WWW
						oldwww.save()
					else:						# новый URL существует в WWW
						if (ContactWWW.objects.filter(contact=object.contact, www__URL=URL).count() == 0): # не существует для этого контакта
							object.www = WWW.objects.get(URL=URL)	# заменить WWW в ContactWWW
							object.save()
						oldwww.delete()				# старый WWW - прибить
				else:							# такой WWW есть только еще у кого-то
					if (WWW.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						object.www = WWW.objects.create(URL=URL)	# создать новый WWW
						object.save()
					else:						# новый URL существует в WWW
						if (ContactWWW.objects.filter(contact=object.contact, www__URL=URL).count() == 0): # не существует для этого контакта
							object.www = WWW.objects.get(URL=URL)	# заменить WWW в ContactWWW
							object.save()
						else:					# существует для этого контакта
							object.delete()			# лишний ContactWWW - прибить
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactWWWForm({'URL': ContactWWW.objects.get(pk=object_id).www.URL})
		objectlist = ContactWWW.objects.get(pk=object_id).www.contactwww_set.exclude(pk=object_id)
	return render_to_response('core/www_form.html', context_instance=RequestContext(request, {'form': form, 'object': object, 'objectlist': objectlist, 'next': next}))

@login_required
def	contact_www_del(request, object_id):
	'''
	object_id - ContactWWW.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	object = ContactWWW.objects.get(pk=object_id)
	contact = object.contact
	if (object.www.contactwww_set.count() > 1):
		object.delete()
	else:
		object.www.delete()
	return HttpResponseRedirect(next)

@login_required
def	contact_email_add(request, object_id):
	'''
	Add new Email to Contact.
	Check exist and uniq pair contact<>email
	@param object_id - Contact.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactEmailForm(request.POST)
		if form.is_valid():
			if (ContactEmail.objects.filter(contact__id=object_id, email__URL=form.cleaned_data['URL']).count() == 0):	# realy new; else - do nothing
				ContactEmail(contact=Contact.objects.get(pk=object_id), email=Email.objects.get_or_create(URL=form.cleaned_data['URL'])[0]).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactEmailForm()
	return render_to_response('core/email_form.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

@login_required
def	contact_email_edit(request, object_id):
	'''
	Edit Contact's email.
	@param object_id:ContactEmail.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	object = ContactEmail.objects.get(pk=object_id)
	if request.method == 'POST':
		objectlist = list()
		form = ContactEmailForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['URL']
			# 1. URL is not the same
			if (URL != object.email.URL):
				oldemail = object.email
				if (oldemail.contactemail_set.count() == 1):		# такой WWW есть только у 1 контакта
					if (Email.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						oldemail.URL = URL			# заменит URL в WWW
						oldemail.save()
					else:						# новый URL существует в WWW
						if (ContactEmail.objects.filter(contact=object.contact, email__URL=URL).count() == 0): # не существует для этого контакта
							object.email = Email.objects.get(URL=URL)	# заменить WWW в ContactWWW
							object.save()
						oldemail.delete()				# старый WWW - прибить
				else:							# такой WWW есть только еще у кого-то
					if (Email.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						object.email = Email.objects.create(URL=URL)	# создать новый WWW
						object.save()
					else:						# новый URL существует в WWW
						if (ContactEmail.objects.filter(contact=object.contact, email__URL=URL).count() == 0): # не существует для этого контакта
							object.email = Email.objects.get(URL=URL)	# заменить WWW в ContactWWW
							object.save()
						else:					# существует для этого контакта
							object.delete()			# лишний ContactWWW - прибить
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactEmailForm({'URL': ContactEmail.objects.get(pk=object_id).email.URL})
		objectlist = ContactEmail.objects.get(pk=object_id).email.contactemail_set.exclude(pk=object_id)
	return render_to_response('core/email_form.html', context_instance=RequestContext(request, {'form': form, 'object': object, 'objectlist': objectlist, 'next': next}))

@login_required
def	contact_email_del(request, object_id):
	'''
	object_id - ContactEmail.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	object = ContactEmail.objects.get(pk=object_id)
	contact = object.contact
	if (object.email.contactemail_set.count() > 1):	# Achtung!
		object.delete()
	else:
		object.email.delete()
	return HttpResponseRedirect(next)

@login_required
def	contact_im_add(request, object_id):
	pass

@login_required
def	contact_im_edit(request, object_id):
	pass

@login_required
def	contact_im_del(request, object_id):
	pass

def	__contact_getabc(request, item_list, formname, fieldname):
	'''
	Handle current ABC page.
	@param request, item_list, formname, fieldname
	@return (abc:int, abc_list:list(dict()))
	'''
	abc_list = list()
	abc = UserSetting.objects.filter(user=User.objects.get(pk=request.user.id), form=formname, action='f', object='abc')
	if (abc):
		abc = int(abc[0].value)
	else:
		abc = 0
	# 2. create ABC list
	# 1st letters of org names
	for a in item_list.extra(select={'abc': 'LEFT(%s, 1)' % fieldname}).distinct().order_by('abc').values_list('abc', flat=True):
		# dict of letter:unicode:active
		if (a):
			abc_list.append({'c': a, 'u': ord(a), 'f': (abc == ord(a))})
	# and everybody
	abc_list.append({'c': '*', 'u': 0, 'f': (abc == 0)})
	return (abc, abc_list)

def	__contact_setabc(request, abc, form):
	'''
	Set new ABC char
	'''
	user = User.objects.get(pk=request.user.id)
	v = int(abc)
	if (v):
		UserSetting.objects.cu_ufa(user=user, form=form, action='f', object='abc', value = v)
	else:
		UserSetting.objects.filter(user=user, form=form, action='f', object='abc').delete()

@login_required
def	org_index(request):
	'''
	request keys:
	a: ABC letter
	'''
	item_list = Org.objects.all()
	abc, abc_list = __contact_getabc(request, item_list, 'org_list', 'name')
	if (abc):
		item_list = item_list.filter(name__startswith=(unichr(abc)))
	return object_list (
		request,
		queryset = item_list,
		template_name = 'contact/org_list.html',
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		extra_context = {
			'abc_list': abc_list,
			't0': time.time()
		}
	)

@login_required
def	org_setabc(request, abc):
	__contact_setabc(request, abc, 'org_list')
	return redirect(org_index)

@login_required
def	org_detail(request, object_id):
	return object_detail (
		request,
		queryset = Org.objects.all(),
		object_id = object_id,
		template_name = 'contact/org_detail.html',
	)

@login_required
def	org_add(request):
	return	create_object (
		request,
		form_class = OrgForm,
		template_name = 'contact/org_form.html',	# FIXME: 
	)

@login_required
def	org_edit(request, object_id):
	return	update_object (
		request,
		form_class = OrgForm,
		object_id = object_id,
		template_name = 'contact/org_form.html',	# FIXME: 
	)

@login_required
def	org_del(request, object_id):
	Org.objects.get(pk=long(object_id)).delete()
	return redirect('apps.contact.views.org_index')

@login_required
def	org_stuff_add(request, object_id):
	'''
	@param object_id:ID - Org id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	object = Org.objects.get(pk=object_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			new_object = form.save(commit=False)
			new_object.org = object
			new_object.save()
			return HttpResponseRedirect(reverse('apps.contact.views.contact_detail', kwargs={'object_id': object.org.id}))
	else:	# GET
		form = OrgStuffForm()
	return render_to_response('contact/org_stuff_form.html', context_instance=RequestContext(request, {'object': object, 'form': form, 'mode': True, 'next': next}))

@login_required
def	org_stuff_edit(request, object_id):
	'''
	Edit Org's stuff.
	@param object_id:OrgStuff.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	object = OrgStuff.objects.get(pk=object_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			object.person=form.cleaned_data['person']
			object.role=form.cleaned_data['role']
			object.save()
			return HttpResponseRedirect(reverse('apps.contact.views.contact_detail', kwargs={'object_id': object.org.id}))
	else:	# GET
		form = OrgStuffForm(instance=object)
	return render_to_response('contact/org_stuff_form.html', context_instance=RequestContext(request, {'object': object, 'form': form, 'next': next}))

@login_required
def	org_stuff_del(request, object_id):
	'''
	@param object_id:ID - OrgStuff id
	'''
	object = OrgStuff.objects.get(pk=object_id)
	org = object.org
	if (object.role.orgstuff_set.count() > 1):	# Achtung!
		object.delete()
	else:
		object.role.delete()
	return redirect(org)

@login_required
def	person_index(request):
	item_list = Person.objects.all()
	abc, abc_list = __contact_getabc(request, item_list, 'person_list', 'lastname')
	if (abc):
		item_list = item_list.filter(lastname__startswith=(unichr(abc)))
	return object_list (
		request,
		queryset = item_list,
		template_name = 'contact/person_list.html',
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		extra_context = {
			'abc_list': abc_list,
			't0': time.time()
		}
	)

@login_required
def	person_setabc(request, abc):
	__contact_setabc(request, abc, 'person_list')
	return redirect(person_index)

@login_required
def	person_detail(request, object_id):
	return object_detail (
		request,
		queryset = Person.objects.all(),
		object_id = object_id,
		template_name = 'contact/person_detail.html',
	)

@login_required
def	person_add(request):
	return	create_object (
		request,
		form_class = PersonForm,
		template_name = 'contact/person_form.html',	# FIXME: 
	)

@login_required
def	person_edit(request, object_id):
	return	update_object (
		request,
		form_class = PersonForm,
		object_id = object_id,
		template_name = 'contact/person_form.html',	# FIXME: 
	)

@login_required
def	person_del(request, object_id):
	print "Person del"
	Person.objects.get(pk=long(object_id)).delete()
	return redirect('apps.contact.views.person_index')

@login_required
def	person_stuff_add(request, object_id):
	'''
	@param object_id:ID - Person id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	object = Person.objects.get(pk=object_id)
	if request.method == 'POST':
		form = PersonStuffForm(request.POST)
		if form.is_valid():
			new_object = form.save(commit=False)
			new_object.person = object
			new_object.save()
			return HttpResponseRedirect(reverse('apps.contact.views.contact_detail', kwargs={'object_id': object.person.id}))
	else:	# GET
		form = PersonStuffForm()
	return render_to_response('contact/person_stuff_form.html', context_instance=RequestContext(request, {'object': object, 'form': form, 'mode': True, 'next': next}))

@login_required
def	person_stuff_edit(request, object_id):
	'''
	Edit Person's stuff.
	@param object_id:OrgStuff.id
	'''
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	object = OrgStuff.objects.get(pk=object_id)
	if request.method == 'POST':
		form = PersonStuffForm(request.POST)
		if form.is_valid():
			object.org=form.cleaned_data['org']
			object.role=form.cleaned_data['role']
			object.save()
			return HttpResponseRedirect(reverse('apps.contact.views.contact_detail', kwargs={'object_id': object.person.id}))
	else:	# GET
		form = PersonStuffForm(instance=object)
	return render_to_response('contact/person_stuff_form.html', context_instance=RequestContext(request, {'object': object, 'form': form, 'next': next}))

@login_required
def	person_stuff_del(request, object_id):
	'''
	@param object_id:ID - OrgStuff id
	'''
	object = OrgStuff.objects.get(pk=object_id)
	person = object.person
	if (object.role.orgstuff_set.count() > 1):	# Achtung!
		object.delete()
	else:
		object.role.delete()
	return redirect(person)

@login_required
def	jobrole_index(request):
	return object_list (
		request,
		queryset = JobRole.objects.all(),
		template_name = 'contact/jobrole_list.html',
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
	)

@login_required
def	jobrole_setabc(request, abc):
	__contact_setabc(request, abc, 'jobrole_list')
	return redirect(jobrole_index)

@login_required
def	jobrole_detail(request, object_id):
	return object_detail (
		request,
		queryset = JobRole.objects.all(),
		object_id = object_id,
		template_name = 'contact/jobrole_detail.html',
	)

@login_required
def	jobrole_add(request):
	return	create_object (
		request,
		form_class = JobRoleForm,
		template_name = 'contact/jobrole_form.html',	# FIXME: 
	)

@login_required
def	jobrole_edit(request, object_id):
	return	update_object (
		request,
		form_class = JobRoleForm,
		object_id = object_id,
		template_name = 'contact/jobrole_form.html',	# FIXME: 
	)

@login_required
def	jobrole_del(request, object_id):
	Org.objects.get(pk=long(object_id)).delete()
	return redirect('apps.contact.views.jobrole_index')

def	dav(request):
	'''
	'''
	print request.method
	func = carddav.davdict.get(request.method, None)
	if func:
		return func(request)
	else:
		raise Http404
