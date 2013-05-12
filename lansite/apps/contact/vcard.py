# -*- coding: utf-8 -*-
'''
lansite.apps.contact.vcard
'''

from django.contrib.auth.decorators import login_required, permission_required

import time, datetime, vobject

@login_required
def	person_vcard_export(request):
	'''
	Export Persons to vCard 3.0 file
	'''
	user = User.objects.get(pk=request.user.id)	# aka author
	response = HttpResponse(mimetype='text/x-vcard')
	response['Content-Disposition'] = '; filename=person.vcf'
	for object in Person.objects.all().order_by('lastname', 'firstname'):
		card = vobject.vCard()
		# N
		card.add('n')
		card.n.value = vobject.vcard.Name(family=object.lastname, given=object.firstname, additional=object.midname)
		# FN
		card.add('fn')
		if (object.firstname):
			card.fn.value = object.firstname
		if (object.midname):
			if (card.fn.value):
				card.fn.value += ' '
			card.fn.value += object.midname
		if (object.lastname):
			if (card.fn.value):
				card.fn.value += ' '
			card.fn.value += object.lastname
		if (object.birthdate):
			card.add('bday')
			card.bday.value = object.birthdate.strftime("%Y-%m-%d")
			#datetime.datetime.strptime(value, "%Y-%m-%d").date()
		# TEL
		if (object.contactphone_set.count()):
			card.add('tel')
			for i, item in enumerate(object.contactphone_set.all()):
				newitem = vobject.base.ContentLine(name = 'tel', params={}, value = item.phone.no)
				if (item.ext):
					newitem.value += (' '+item.ext)
				#newitem.params['type'].append('HOME')
				if (i):
					card.contents['tel'].append(newitem)
				else:
					card.contents['tel'][0] = newitem
		# EMAIL
		if (object.contactemail_set.count()):
			card.add('email')
			for i, item in enumerate(object.contactemail_set.all()):
				newitem = vobject.base.ContentLine(name = 'email', params={}, value = item.email.URL)
				newitem.type_param = 'INTERNET'
				if (i):
					card.contents['email'].append(newitem)
				else:
					card.contents['email'][0] = newitem
		# URL
		if (object.contactwww_set.count()):
			card.add('url')
			for i, item in enumerate(object.contactwww_set.all()):
				newitem = vobject.base.ContentLine(name = 'url', params={}, value = item.www.URL)
				if (i):
					card.contents['url'].append(newitem)
				else:
					card.contents['url'][0] = newitem
		# <IM>
		if (object.contactim_set.count()):
			for item in object.contactim_set.all():
				imtype = "x-" + item.im.type.name.encode('ascii', 'ignore').lower()
				newitem = vobject.base.ContentLine(name = imtype, params={}, value = item.im.account)
				if imtype in card.contents:
					card.contents[imtype].append(newitem)
				else:
					card.add(imtype)
					card.contents[imtype][0] = newitem
		# ORG + TITLE (1)
		if (object.orgstuff_set.count()):
			card.add('org')
			card.add('title')
			for i, item in enumerate(object.orgstuff_set.all()):
				newitem = vobject.base.ContentLine(name = 'org', params={}, value = item.org.name)
				if (i):
					card.contents['org'].append(newitem)
				else:
					card.contents['org'][0] = newitem
				if (not card.title.value):
					card.title.value = item.role.name
		# ADR
		# Future:
			# ROLE (обязанности)
			# CATEGORIES
			# NOTE
			# REV:date
			# CLASS: "PUBLIC" / "PRIVATE" / "CONFIDENTIAL"
			# SORT-STRING: ?
			# KEY - public key cert
			# NICNAME
			# PHOTO
			# GEO
		# Skip:
			# MAILER
			# TZ
			# LOGO
			# AGENT
			# PRODID
			# SOUND
			# UID
		response.write(card.serialize())
	return response

@login_required
def	person_vcard_import(request):
	'''
	Import Persons from vCard 3.0 format
	'''
	result = list()
	skipset = set(('FN', 'N', 'NICKNAME', 'NOTE', 'VERSION', 'X-ABDATE', 'X-ABLABEL', 'X-ABRELATEDNAMES', 'X-PHONETIC-FIRST-NAME', 'X-PHONETIC-LAST-NAME'))	# set of parms to skip
	imset = set(('X-GTALK', 'X-ICQ', 'X-JABBER'))	# set of IMs
	if (request.method == 'POST'):
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			user = User.objects.get(pk=request.user.id)
			for card in vobject.readComponents(file.read()):
				if (not card.contents['fn'][0].value):
					continue	# skip empty
				value = card.contents['n'][0].value
				person = Person.objects.get_or_create(firstname = value.given[:16], midname = value.additional[:24], lastname = value.family[:24])[0]
				orgs = dict()	# name: Org
				title = None
				# skip suffix, prefix; vobject.vcard.Name
				for parm in card.contents:
					for p in card.contents[parm]:	# vobject.base.ContentLine
						#print p.name, u':', p.value, p.params
						name = p.name
						value = p.value
						# TODO: tel, addr
						# TODO: types: tel, email, url, addr
						if (name == 'ADR'):			# *, vobject.vcard.Address, typed
							'''
							extended, box, city, code, country, region, street
							box: post-office-box (п/я)?
							extended: квартира/офис|что угодно
							street: улица (с домом?)
							city|locality: город|населенный пункт
							region: область/штат
							code: postal сode (почтовый индекс)?
							country: страна
							Types: [DOM INTL POSTAL PARCEL] HOME WORK
							'''
							#for i in value.__dict__.keys():
							#	print u'\t%s: %s' % (i, value.__dict__[i])
							pass
						elif (name == 'BDAY'):			# 1?
							bday = datetime.datetime.strptime(value, "%Y-%m-%d").date()
							if person.birthdate != bday:
								person.birthdate = bday
								person.save()
						elif (name == 'EMAIL'):			# *, typed
							# types: AOL AppleLink ATTMail CIS eWorld INTERNET IBMMail MCIMail POWERSHARE PRODIGY TLX X400
							# types: HOME WORK
							ContactEmail.objects.get_or_create(contact=person, email=(Email.objects.get_or_create(URL=value)[0]))
						elif (name == 'ORG'):			# 1?, list
							for i in value:
								orgs[i] = Org.objects.get_or_create(name=i)[0]
						elif (name == 'TEL'):			# *, typed
							# types: PREF WORK HOME VOICE FAX MSG CELL PAGER BBS MODEM CAR ISDN VIDEO
							# FIXME: translate(), maketrans()
							# FIXME: dtmf
							no = value.encode('ascii', 'ignore').strip()
							if (len(no) > 15):
								newno = ''
								for c in no:
									if c.isdigit():
										newno += c
									elif (c == '+' and not newno):
										newno += c
								no = newno[:16]
							ContactPhone.objects.get_or_create(contact=person, phone=(Phone.objects.get_or_create(no=no)[0]))
						elif (name == 'TITLE'):			# 1?
							title = value
						elif (name == 'URL'):			# *, typed
							# types: WORK
							ContactWWW.objects.get_or_create(contact=person, www=(WWW.objects.get_or_create(URL=value)[0]))
						elif (name in imset):			# *
							ContactIM.objects.get_or_create(contact=person, im=(
								IM.objects.get_or_create(account=value, type=(
									IMType.objects.get(name=name[2:])
								))[0])
							)
						elif (name in skipset):	# 
							pass	# skip
						else:
							print 'Unknown key', name, ':', value
				#person.save()
				# link person to orgs
				if (title):
					for org in orgs.values():
						OrgStuff.objects.get_or_create(
							org = org,
							person=person,
							role=(
								JobRole.objects.get_or_create(name=title)[0])
						)
			return redirect('apps.contact.views.person_index')
	else:
		form = FileUploadForm()
	return render_to_response('contact/person_vcard_upload.html', context_instance=RequestContext(request, {'form': form, 'result': result}))

