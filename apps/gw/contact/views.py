# -*- coding: utf-8 -*-
'''
lansite.gw.contact.views.py
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

# 2. python
from urlparse import urlparse

# 3. my
from models import *
from forms import *

# 4. siblings
from gw.bits.views import any_idx, any_dtl

def	contact_index(request):
	return any_idx(request, 'contact', Contact)

def	contact_detail(request, item_id):
	if (Contact.objects.get(pk=item_id).get_real_instance_class() == Person):
		return person_detail(request, item_id)
	else:
		return org_detail(request, item_id)

def	contact_add(request):
	return any_add(request, 'contact', Contact, ContactForm)

def	contact_edit(request, item_id):
	if (Contact.objects.get(pk=item_id).get_real_instance_class() == Person):
		return person_edit(request, item_id)
	else:
		return org_edit(request, item_id)

def	contact_del(request, item_id):
	if (Contact.objects.get(pk=item_id).get_real_instance_class() == Person):
		return person_del(request, item_id)
	else:
		return org_del(request, item_id)

def	contact_addr_edit(request, item_id):
	'''
	Change address of Contact
	@param item_id:int - ContactAddr.id
	@param ?address=<int> - Address to change to
	If address not changed - nothing to do
	If address already exists - delete old
	Else - change to new
	'''
	item = ContactAddr.objects.get(pk=item_id)
	contact = item.contact
	old_address = item.addr
	address_id = request.REQUEST.get('address', None)
	if (address_id):
		new_address = Address.objects.get(pk=address_id)
		if (new_address != old_address):
			if (contact.contactaddr_set.filter(addr=new_address).count()):	# already exists
				item.delete()
			else:
				item.addr = new_address
				item.save()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_addr_del(request, item_id):
	'''
	Delete address of Contact
	@param item_id:int - ContactAddr.id
	'''
	item = ContactAddr.objects.get(pk=item_id)
	contact = item.contact
	item.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_addr_add(request, item_id):
	'''
	Add address to contact callback w/ ?address=<selected address id>
	@param item_id - contact id
	@param ?address=<int> - address to add
	'''
	contact = Contact.objects.get(pk=item_id)
	address_id = request.REQUEST.get('address', None)
	if (address_id):
		address = Address.objects.get(pk=address_id)
		item = ContactAddr.objects.create(contact=contact, addr=address)
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_phone_add(request, item_id):
	'''
	Add new Phone to Contact.
	@param item_id - Contact.id
	FIXME: types
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactPhoneForm(request.POST)
		if form.is_valid():
			q = ContactPhone.objects.filter(contact__id=item_id, phone__no=form.cleaned_data['no'])
			if (q.count() == 0):	# realy new; else - do nothing
				ContactPhone(contact=Contact.objects.get(pk=item_id), phone=Phone.objects.get_or_create(no=form.cleaned_data['no'])[0], ext=form.cleaned_data['ext']).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactPhoneForm()
	return render_to_response('gw/phone_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

def	contact_phone_edit(request, item_id):
	'''
	Edit Contact's phone.
	@param item_id:ContactPhone.id
	FIXME: types
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	item = ContactPhone.objects.get(pk=item_id)
	if request.method == 'POST':
		itemlist = list()	# what is it?
		form = ContactPhoneForm(request.POST)
		if form.is_valid():
			no = form.cleaned_data['no']
			# 1. no is not the same
			if (no != item.phone.no):
				oldphone = item.phone
				if (oldphone.contactphone_set.count() == 1):		# такой no есть только у 1 контакта
					if (Phone.objects.filter(no=no).count() == 0):	# новый no не существует в Phone
						oldphone.no = no			# заменит no в Phone
						oldphone.save()
					else:						# новый no существует в Phone
						if (ContactPhone.objects.filter(contact=item.contact, phone__no=no).count() == 0): # не существует для этого контакта
							item.phone = Phone.objects.get(no=no)	# заменить Phone в ContactPhone
							item.save()
						oldphone.delete()				# старый WWW - прибить
				else:							# такой Phone есть только еще у кого-то
					if (Phone.objects.filter(no=no).count() == 0):	# новый no не существует в Phone
						item.phone = Phone.objects.create(no=no)	# создать новый Phone
						item.save()
					else:						# новый no существует в Phone
						if (ContactPhone.objects.filter(contact=item.contact, phone__no=no).count() == 0): # не существует для этого контакта
							item.phone = Phone.objects.get(no=no)	# заменить Phone в ContactPhone
							item.save()
						else:					# существует для этого контакта
							item.delete()			# лишний ContactPhone - прибить
			else:	# no is the same
				ext = form.cleaned_data['ext']
				if (ext != item.ext):
					item.ext = ext
					item.save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactPhoneForm({'no': item.phone.no, 'ext': item.ext})
		itemlist = item.phone.contactphone_set.exclude(pk=item_id)
	return render_to_response('gw/phone_edit.html', context_instance=RequestContext(request, {'form': form, 'item': item, 'itemlist': itemlist, 'next': next}))

def	contact_phone_del(request, item_id):
	'''
	item_id - ContactPhone.id
	'''
	item = ContactPhone.objects.get(pk=item_id)
	contact = item.contact
	if (item.phone.contactphone_set.count() > 1):
		item.delete()
	else:
		item.phone.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_www_add(request, item_id):
	'''
	Add new WWW to Contact.
	Check exist and uniq pair contact<>www
	@param item_id - Contact.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactWWWForm(request.POST)
		if form.is_valid():
			if (ContactWWW.objects.filter(contact__id=item_id, www__URL=form.cleaned_data['URL']).count() == 0):	# realy new; else - do nothing
				ContactWWW(contact=Contact.objects.get(pk=item_id), www=WWW.objects.get_or_create(URL=form.cleaned_data['URL'])[0]).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactWWWForm()
	return render_to_response('gw/www_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

def	contact_www_edit(request, item_id):
	'''
	Edit Contact's www.
	@param item_id:ContactWWW.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	item = ContactWWW.objects.get(pk=item_id)
	if request.method == 'POST':
		itemlist = list()
		form = ContactWWWForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['URL']
			# 1. URL is not the same
			if (URL != item.www.URL):
				oldwww = item.www
				if (oldwww.contactwww_set.count() == 1):		# такой WWW есть только у 1 контакта
					if (WWW.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						oldwww.URL = URL			# заменит URL в WWW
						oldwww.save()
					else:						# новый URL существует в WWW
						if (ContactWWW.objects.filter(contact=item.contact, www__URL=URL).count() == 0): # не существует для этого контакта
							item.www = WWW.objects.get(URL=URL)	# заменить WWW в ContactWWW
							item.save()
						oldwww.delete()				# старый WWW - прибить
				else:							# такой WWW есть только еще у кого-то
					if (WWW.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						item.www = WWW.objects.create(URL=URL)	# создать новый WWW
						item.save()
					else:						# новый URL существует в WWW
						if (ContactWWW.objects.filter(contact=item.contact, www__URL=URL).count() == 0): # не существует для этого контакта
							item.www = WWW.objects.get(URL=URL)	# заменить WWW в ContactWWW
							item.save()
						else:					# существует для этого контакта
							item.delete()			# лишний ContactWWW - прибить
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactWWWForm({'URL': ContactWWW.objects.get(pk=item_id).www.URL})
		itemlist = ContactWWW.objects.get(pk=item_id).www.contactwww_set.exclude(pk=item_id)
	return render_to_response('gw/www_edit.html', context_instance=RequestContext(request, {'form': form, 'item': item, 'itemlist': itemlist, 'next': next}))

def	contact_www_del(request, item_id):
	'''
	item_id - ContactWWW.id
	'''
	item = ContactWWW.objects.get(pk=item_id)
	contact = item.contact
	if (item.www.contactwww_set.count() > 1):
		item.delete()
	else:
		item.www.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_email_add(request, item_id):
	'''
	Add new Email to Contact.
	Check exist and uniq pair contact<>email
	@param item_id - Contact.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	if request.method == 'POST':
		form = ContactEmailForm(request.POST)
		if form.is_valid():
			if (ContactEmail.objects.filter(contact__id=item_id, email__URL=form.cleaned_data['URL']).count() == 0):	# realy new; else - do nothing
				ContactEmail(contact=Contact.objects.get(pk=item_id), email=Email.objects.get_or_create(URL=form.cleaned_data['URL'])[0]).save()
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactEmailForm()
	return render_to_response('gw/email_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': True, 'next': next}))

def	contact_email_edit(request, item_id):
	'''
	Edit Contact's email.
	@param item_id:ContactEmail.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	item = ContactEmail.objects.get(pk=item_id)
	if request.method == 'POST':
		itemlist = list()
		form = ContactEmailForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['URL']
			# 1. URL is not the same
			if (URL != item.email.URL):
				oldemail = item.email
				if (oldemail.contactemail_set.count() == 1):		# такой WWW есть только у 1 контакта
					if (Email.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						oldemail.URL = URL			# заменит URL в WWW
						oldemail.save()
					else:						# новый URL существует в WWW
						if (ContactEmail.objects.filter(contact=item.contact, email__URL=URL).count() == 0): # не существует для этого контакта
							item.email = Email.objects.get(URL=URL)	# заменить WWW в ContactWWW
							item.save()
						oldemail.delete()				# старый WWW - прибить
				else:							# такой WWW есть только еще у кого-то
					if (Email.objects.filter(URL=URL).count() == 0):	# новый URL не существует в WWW
						item.email = Email.objects.create(URL=URL)	# создать новый WWW
						item.save()
					else:						# новый URL существует в WWW
						if (ContactEmail.objects.filter(contact=item.contact, email__URL=URL).count() == 0): # не существует для этого контакта
							item.email = Email.objects.get(URL=URL)	# заменить WWW в ContactWWW
							item.save()
						else:					# существует для этого контакта
							item.delete()			# лишний ContactWWW - прибить
			return HttpResponseRedirect(next)
	else:	# GET
		form = ContactEmailForm({'URL': ContactEmail.objects.get(pk=item_id).email.URL})
		itemlist = ContactEmail.objects.get(pk=item_id).email.contactemail_set.exclude(pk=item_id)
	return render_to_response('gw/email_edit.html', context_instance=RequestContext(request, {'form': form, 'item': item, 'itemlist': itemlist, 'next': next}))

def	contact_email_del(request, item_id):
	'''
	item_id - ContactEmail.id
	'''
	item = ContactEmail.objects.get(pk=item_id)
	contact = item.contact
	if (item.email.contactemail_set.count() > 1):	# Achtung!
		item.delete()
	else:
		item.email.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': contact.id}))

def	contact_im_add(request, item_id):
	pass

def	contact_im_edit(request, item_id):
	pass

def	contact_im_del(request, item_id):
	pass

def	org_index(request):
	return any_idx(request, 'org', Org)

def	org_detail(request, item_id):
	return any_dtl(request, 'org', Org, item_id)

def	org_add(request):
	return any_add(request, 'org', Org, OrgForm)

def	org_edit(request, item_id):
	return any_edt(request, 'org', Org, OrgForm, item_id)

def	org_del(request, item_id):
	return any_del(request, 'org', Org, item_id)

def	org_stuff_add(request, item_id):
	'''
	@param item_id:ID - Org id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	item = Org.objects.get(pk=item_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = item
			new_item.save()
			return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': item.org.id}))
	else:	# GET
		form = OrgStuffForm()
	return render_to_response('gw/org_stuff_edit.html', context_instance=RequestContext(request, {'item': item, 'form': form, 'mode': True, 'next': next}))

def	org_stuff_edit(request, item_id):
	'''
	Edit Org's stuff.
	@param item_id:OrgStuff.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	item = OrgStuff.objects.get(pk=item_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			item.person=form.cleaned_data['person']
			item.role=form.cleaned_data['role']
			item.save()
			return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': item.org.id}))
	else:	# GET
		form = OrgStuffForm(instance=item)
	return render_to_response('gw/org_stuff_edit.html', context_instance=RequestContext(request, {'item': item, 'form': form, 'next': next}))

def	org_stuff_del(request, item_id):
	'''
	@param item_id:ID - OrgStuff id
	'''
	item = OrgStuff.objects.get(pk=item_id)
	org = item.org
	if (item.role.orgstuff_set.count() > 1):	# Achtung!
		item.delete()
	else:
		item.role.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': org.id}))

def	person_index(request):
	return any_idx(request, 'person', Person)

def	person_detail(request, item_id):
	return any_dtl(request, 'person', Person, item_id)

def	person_add(request):
	return any_add(request, 'person', Person, PersonForm)

def	person_edit(request, item_id):
	return any_edt(request, 'person', Person, PersonForm, item_id)

def	person_del(request, item_id):
	return any_del(request, 'person', Person, item_id)

def	person_stuff_add(request, item_id):
	'''
	@param item_id:ID - Person id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	item = Person.objects.get(pk=item_id)
	if request.method == 'POST':
		form = PersonStuffForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.person = item
			new_item.save()
			return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': item.person.id}))
	else:	# GET
		form = PersonStuffForm()
	return render_to_response('gw/person_stuff_edit.html', context_instance=RequestContext(request, {'item': item, 'form': form, 'mode': True, 'next': next}))

def	person_stuff_edit(request, item_id):
	'''
	Edit Person's stuff.
	@param item_id:OrgStuff.id
	'''
	next = request.REQUEST.get('next', None)
	if (next == None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	error = None
	item = OrgStuff.objects.get(pk=item_id)
	if request.method == 'POST':
		form = PersonStuffForm(request.POST)
		if form.is_valid():
			item.org=form.cleaned_data['org']
			item.role=form.cleaned_data['role']
			item.save()
			return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': item.person.id}))
	else:	# GET
		form = PersonStuffForm(instance=item)
	return render_to_response('gw/person_stuff_edit.html', context_instance=RequestContext(request, {'item': item, 'form': form, 'next': next}))

def	person_stuff_del(request, item_id):
	'''
	@param item_id:ID - OrgStuff id
	'''
	item = OrgStuff.objects.get(pk=item_id)
	person = item.person
	if (item.role.orgstuff_set.count() > 1):	# Achtung!
		item.delete()
	else:
		item.role.delete()
	return HttpResponseRedirect(reverse('gw.views.contact_detail', kwargs={'item_id': person.id}))

def	jobrole_index(request):
	return any_idx(request, 'jobrole', JobRole)

def	jobrole_detail(request, item_id):
	return any_dtl(request, 'jobrole', JobRole, item_id)

def	jobrole_add(request):
	return any_add(request, 'jobrole', JobRole, JobRoleForm)

def	jobrole_edit(request, item_id):
	return any_edt(request, 'jobrole', JobRole, JobRoleForm, item_id)

def	jobrole_del(request, item_id):
	return any_del(request, 'jobrole', JobRole, item_id)
