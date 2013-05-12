# -*- coding: utf-8 -*-
'''
lansite.apps.address.views.py
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext

# 2. python
from urlparse import urlparse

# 3. my
from models import *
from forms import *

# 4. siblings
#from views

@login_required
def	contact_address_add(request, contact_id):

	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	
	org = Org.objects.get(id=contact_id)
	
	formaddresstype = ContactAddressTypeForm()
	formaddresstype.setdata(contact_id)
	
	form=SelectAddressTypeForm()
	form.setdata(170)
	return render_to_response('gw/address/address_add.html', context_instance=RequestContext(request, {
        'next': next,
        'form': form,
        'org':org,
        'formaddresstype': formaddresstype,
    }))


@login_required
def	address_getaddress(request, parent_id, type_id):

	form=SelectAddressForm()
	form.setdata(parent_id, type_id)
	return HttpResponse(form)

@login_required
def	address_gettype(request, parent_id):

	form=SelectAddressTypeForm()
	form.setdata(parent_id)
	return HttpResponse(form)

@login_required
def	address_getalltypes(request):

	form=SelectAddressTypeForm()
	form.setdata(None)
	return HttpResponse(form)

@login_required
def	address_getcountry(request):

	form=SelectAddressForm()
	form.setdata(None, None)
	return HttpResponse(form)

@login_required
def	address_getzip(request, address_id):
	
	zip = Address.objects.get(id=address_id).zip
	return HttpResponse(zip)
		
@login_required
def	contact_address_edit(request, contact_id):

	return HttpResponse()

@login_required
def	contact_address_save(request, contact_id):
	
	post = request.POST.items()
	import simplejson
	data = simplejson.loads(str(post[0][0].encode('utf-8')),'utf8')
	
	org = Org.objects.get(pk=contact_id)
	
	i = 5
	while i >= 1:
		if 'divType' + str(i) in data:
			lastAddressNumber = i
			break
		i = i - 1
	
	if not 'divTypeAdd1' in data:
		address = Address.objects.get(pk=data['divAddress' + str(lastAddressNumber)])
		
		address.endpoint = True
		
		try:
			contactaddr = ContactAddr.objects.get(contact=org, addr=address)
		except:
			contactaddr = ContactAddr()
			contactaddr.contact = org
			contactaddr.addr = address
			contactaddr.save()
			
		for contactaddrtype in ContactAddrType.objects.all():
			if 'Type' + str(contactaddrtype.id) in data:
				contact2addrtype = Contact2AddrType()
				contact2addrtype.type = contactaddrtype
				contact2addrtype.caddr = contactaddr
				contact2addrtype.save()
				# to delete in future releases {
				if contactaddrtype.name == u"Юридический":
					org.laddress = str(address.zip) + ', ' + address.getfullname()
					org.save()
				elif contactaddrtype.name == u"Фактический":
					org.raddress = str(address.zip) + ', ' + address.getfullname()
					org.save()					
				# } to delete in future releases 
		
	else:
		j = 1
		while j <= 6:
			if 'divTypeAdd' + str(j) in data:				
				try:
					if j == 1:
						parent = Address.objects.get(pk=data['divAddress' + str(lastAddressNumber)])
					name = data['divAddressAdd' + str(j)]
					type = AddrShort.objects.get(pk=data['divTypeAdd' + str(j)])
					try:
						address = Address.objects.get(name=name,type=type,parent=parent)
					except:
						address = Address()
						address.name = name
						address.type = type
						address.parent = parent
						address.publish = True
						if not 'divTypeAdd' + str(j+1) in data:
							address.endpoint = True
						address.zip = data['zip']
						address.can_delete = True			
						address.save()
				except Exception,e:
					return HttpResponse(e)
				
				parent = address
			
				if not 'divTypeAdd' + str(j+1) in data:
					try:
						contactaddr = ContactAddr.objects.get(contact=org, addr=address)
					except:					
						contactaddr = ContactAddr()
						contactaddr.contact = org
						contactaddr.addr = address
						contactaddr.save()
					
					for contactaddrtype in ContactAddrType.objects.all():
						if 'Type' + str(contactaddrtype.id) in data:
							contact2addrtype = Contact2AddrType()
							contact2addrtype.type = contactaddrtype
							contact2addrtype.caddr = contactaddr
							contact2addrtype.save()
							# to delete in future releases {
							if contactaddrtype.name == u"Юридический":
								org.laddress = str(address.zip) + ', ' + address.getfullname()
								org.save()
							elif contactaddrtype.name == u"Фактический":
								org.raddress = str(address.zip) + ', ' + address.getfullname()
								org.save()				
							# } to delete in future releases 				
				j = j + 1
			
			else:
				break
					
	return HttpResponse('Success')

@login_required
def	contact_address_delete(request, contact_id, address_id):
	
	next = request.REQUEST.get('next', None)
	if (next is None):
		return HttpResponseRedirect(request.path + '?next=%s' % urlparse(request.META.get('HTTP_REFERER', None))[2])
	
	address = Address.objects.get(pk=address_id)
	org = Org.objects.get(pk=contact_id)
	
	contactaddress = ContactAddr.objects.get(contact__id=org.id,addr__id=address.id)
	
	for contact2addrtype in contactaddress.contact2addrtype_set.all():
		contact2addrtype.delete()
		# to delete in future releases {
		if contact2addrtype.type.name == u"Юридический":
			org.laddress = ''
			org.save()
		elif contact2addrtype.type.name == u"Фактический":
			org.raddress = ''
			org.save()					
		# } to delete in future releases 
	
	contactaddress.delete()
	
	if address.can_delete and address.contactaddr_set.count() == 0:
		address.delete()
	
	return redirect(next + '#address')
