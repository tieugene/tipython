#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Stage #3: import sqlite into models

Usage:
./dothis drop && ./dothis sync && ./import.py _bin/data.db

TODO:
* Капитально пропатчить районы брянской области (15200): http://www.sirius-nt.ru/main.asp?sid=QR57R2R00J67J3SW&em=1_M1100_M1154

+	django_content_type - preloaded
	auth_permission (Permission - add/edit/del per each ct) - preloaded
	auth_group (Group)
	auth_group_permissions (Group.m2m.Permission)
	auth_user (User)
	auth_user_groups (User.m2m.Group)
	auth_user_user_permissions (User.m2m.Permission)
	ref_*
	gw_
	django_admin_log
	[django_site?]

Test (P4-2.93, kladr):
	time: 45'53"
'''
import os, sys, re, sqlite3, bsddb, pprint
from datetime import datetime
from django.core.management import setup_environ

import settings
setup_environ(settings)
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction, reset_queries
from objectpermissions.models import UserPermission, GroupPermission

from _import.utility import *

from gw.models import *
from ref.models import *

reload(sys)
sys.setdefaultencoding("utf-8")

settings.DEBUG = False

# global vars
db = None
ct_cache = dict()
pk_cache = None

def	log(s):
	print >> sys.stderr, s, ":", now(), getusedmem()

class	SqliteStorage:
	def	__init__(self):
		self.con = None
		self.cur = None
	def	init(self, dbname):
		self.con = sqlite3.connect(dbname)
		self.cur = self.con.cursor()
	def	get_ct(self):
		'''
		@return [(id, app_label, model),] of ContentType
		'''
		return self.cur.execute("SELECT d0.record, d1.value, d0.value FROM data AS d0 JOIN (SELECT model, record, value FROM data WHERE model='django_content_type' AND field='app_label') AS d1 ON d0.model=d1.model AND d0.record=d1.record WHERE d0.model='django_content_type' AND d0.field='model';").fetchall()
	def	get_perm(self):
		'''
		@return [(id, content_type_id, codename),] of Permission
		'''
		return self.cur.execute("SELECT d0.record, d1.value, d0.value FROM data AS d0 JOIN (SELECT model, record, value FROM data WHERE model='auth_permission' AND field='content_type_id') AS d1 ON d0.model=d1.model AND d0.record=d1.record WHERE d0.model='auth_permission' AND d0.field='codename';").fetchall()
	def	get_list(self, modelname):
		return self.con.cursor().execute("SELECT * FROM data WHERE model=?;", (modelname,))
	def	get_idlist(self, modelname):
		return self.con.cursor().execute("SELECT DISTINCT record FROM data WHERE model=? ORDER BY record;", (modelname,))
	def	get_idplist(self, modelname):
		return self.con.cursor().execute("SELECT DISTINCT record FROM data WHERE model=? AND field='parent_id' ORDER BY CAST(value AS INTEGER), record;", (modelname,))
	def	get_fields(self, modelname, id):
		return dict(self.con.cursor().execute("SELECT field, value FROM data WHERE model=? AND record=?;", (modelname, id)).fetchall())

class	CacheRAM(object):
	def	__init__(self):
		self.data = dict()

	def	set(self, table, key, value):
		if table not in self.data:
			self.data[table] = dict()
		self.data[table][key] = value

	def	get(self, table, key):
		return self.data[table].get(key, None)

	def	copy(self, table0, table1):
		if table0 not in self.data:
			self.data[table0] = dict()
		if table1 in self.data:
			self.data[table0].update(self.data[table1])

class	CacheBDB(object):
	def	__init__(self):
		self.data = bsddb.btopen('tmp.db', 'c')

	def	set(self, table, key, value):
		self.data['%s%016X' % (table, key)] = str(value)

	def	get(self, table, key):
		return long(self.data['%s%016X' % (table, key)])

def	ct():
	'''
	old_id => new_id of ContentType
	'''
	global db, pk_cache, ct_cache
	modelname = 'django_content_type'
	log(modelname)
	for i in (db.get_ct()):
		item = ContentType.objects.get(app_label=i[1], model=i[2])
		ct_cache[item.pk] = item
		pk_cache.set(modelname, i[0], item.pk)
	# X. django_session - skipped
	# X. django_site - ?
	# django_admin_log - ...

@transaction.commit_on_success
def	auth():
	'''
	old_id => new_id of Permission
	'''
	global db, pk_cache
	# 1. Permissions
	modelname = 'auth_permission'
	log(modelname)
	for i in (db.get_perm()):
		pk_cache.set(modelname, i[0], Permission.objects.get(content_type=ContentType.objects.get(pk=pk_cache.get('django_content_type', int(i[1]))), codename=i[2]).pk)
	# 2. Group
	modelname = 'auth_group'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Group.objects.create(
			name = v['name']
		).pk)
	# 3. Group.Permissions
	modelname = 'auth_group_permissions'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		Group.objects.get(pk=pk_cache.get('auth_group',v['group_id'])).permissions.add(Permission.objects.get(pk=pk_cache.get('auth_permission', v['permission_id'])))
	# 4. User
	modelname = 'auth_user'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], User.objects.create(
			username =	v['username'],
			first_name =	v['first_name'],
			last_name =	v['last_name'],
			email =		v['email'],
			password =	v['password'],
			is_staff =	v['is_staff'],
			is_active =	v['is_active'],
			is_superuser =	v['is_superuser'],
			last_login =	v['last_login'],
			date_joined =	v['date_joined']
		).pk)
	# 5. User.Group
	modelname = 'auth_user_groups'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		User.objects.get(pk=pk_cache.get('auth_user', v['user_id'])).groups.add(Group.objects.get(pk=pk_cache.get('auth_group', v['group_id'])))
	# 6. User.Permissions
	modelname = 'auth_user_user_permissions'
	log(modelname)
	for p in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		User.objects.get(pk=pk_cache.get('auth_user', v['user_id'])).permissions.add(Permission.objects.get(pk=pk_cache('auth_permission', v['permission_id'])))
	# X. auth_message - skipped

@transaction.commit_on_success
def	okato():
	global db, pk_cache
	modelname = 'ref_okato'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		#if (v['parent_id'] and (not long(v['parent_id']) in data[modelname])):
		#	print i[0], ">", v['parent_id'], "skipped"
		pk_cache.set(modelname, i[0], Okato.objects.create(
			id = i[0],
			parent_id = pk_cache.get(modelname, long(v['parent_id'])) if v['parent_id'] else None,
			code = v['code'],
			name = v['name'],
			comments = v['comments']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	okopf():
	global db, pk_cache
	modelname = 'ref_okopf'
	log(modelname)
	for i in (db.get_idplist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Okopf.objects.create(
			id = i[0],
			parent_id = pk_cache.get(modelname, long(v['parent_id'])) if v['parent_id'] else None,
			name = v['name'],
			shortname = v['shortname'],
			disabled = v['disabled']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	oksm():
	global db, pk_cache
	modelname = 'ref_oksm'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Oksm.objects.create(
			id=i[0],
			alpha2 = v['alpha2'],
			alpha3 = v['alpha3'],
			name = v['name'],
			fullname = v['fullname']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	okved():
	global db, pk_cache
	modelname = 'ref_okved'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Okved.objects.create(
			id = i[0],
			comments = v['comments']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	kladr():
	global db, pk_cache
	# 0
	modelname = 'ref_kladrshort'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], KladrShort.objects.create(
			name = v['name'],
			fullname = v['fullname']
		).pk)
	# 1
	modelname = 'ref_kladrstatetype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], KladrStateType.objects.create(
			id = i[0],
			comments = v['comments']
		).pk)
	reset_queries()
	# 2
	modelname = 'ref_kladr'
	log(modelname)
	idlist = db.get_idlist(modelname)
	for n, i in enumerate(idlist):
		v = db.get_fields(modelname, i[0])
		Kladr.objects.create(
			id = i[0],
			parent_id = v['parent_id'] if v['parent_id'] else None,
			name = v['name'],
			short_id = pk_cache.get('ref_kladrshort', int(v['short_id'])) if v['short_id'] else None,
			zip = v['zip'],
			center_id = pk_cache.get('ref_kladrstatetype', int(v['center_id'])) if v['center_id'] else None
		)
	reset_queries()
	# 3
	modelname = 'ref_kladokato'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		KladrOkato.objects.create(
			kladr_id = i[0],
			okato = long(v['okato'])
		)
	# x. that's all
	reset_queries()

@transaction.commit_manually
def	address():
	global db, pk_cache
	# 0
	modelname = 'gw_addrshort'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], AddrShort.objects.create(
			name = v['name'],
			fullname = v['fullname']
		).pk)
	transaction.commit()
	reset_queries()
	# 1
	modelname = 'gw_addrtype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], AddrType.objects.create(
			abbr = v['abbr'],
			name = v['name']
		).pk)
	transaction.commit()
	reset_queries()
	# 2
	modelname = 'gw_address'
	log(modelname)
	for n, i in enumerate(db.get_idplist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Address.objects.create(
			name = v['name'],
			type_id = pk_cache.get('gw_addrshort', int(v['type_id'])) if v['type_id'] else None,
			typeplace = v['typeplace'],
			parent_id = pk_cache.get(modelname, long(v['parent_id'])) if v['parent_id'] else None,
			publish = v['publish'],
			endpoint = v['endpoint'],
			zip = v['zip'],
			fullname = v['fullname']
		).pk)
		if (n % 100000 == 99999):
			log("Commiting %d" % (n + 1))
			transaction.commit()
			log("Commited")
	transaction.commit()
	reset_queries()
	# 3
	modelname = 'gw_addrkladr'
	log(modelname)
	for i in (db.get_idplist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], AddrKladr.objects.create(
			address_id = pk_cache.get('gw_address', long(v['address_id'])),
			kladr_id = v['kladr_id']
		).pk)
	transaction.commit()
	reset_queries()

@transaction.commit_on_success
def	phone():
	global db, pk_cache
	# 0
	modelname = 'gw_phonetype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], PhoneType.objects.create(
			abbr = v['abbr'],
			name = v['name']
		).pk)
	# 1
	modelname = 'gw_phone'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Phone.objects.create(
			abbr = v['no']
		).pk)
	# 2
	modelname = 'gw_phone2type'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Phone2Type.objects.create(
			type_id = pk_cache.get('gw_phonetype', int(v['type_id'])),
			phone_id = pk_cache.get('gw_phone', int(v['phone_id']))
		).pk)
	reset_queries()

@transaction.commit_on_success
def	www():
	global db, pk_cache
	# 0
	modelname = 'gw_www'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], WWW.objects.create(
			URL = v['URL']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	email():
	global db, pk_cache
	# 0
	modelname = 'gw_email'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Email.objects.create(
			URL = v['URL']
		).pk)
	reset_queries()

@transaction.commit_on_success
def	im():
	global db, pk_cache
	# 0
	modelname = 'gw_imtype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], IMType.objects.create(
			name = v['name'],
			comments = v['comments']
		).pk)
	# 1
	modelname = 'gw_im'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], WWW.objects.create(
			account = v['account'],
			type_id = pk_cache.get('gw_imtype', int(v['type_id'])),
		).pk)
	reset_queries()

@transaction.commit_on_success
def	task():
	global db, pk_cache
	# 0
	modelname = 'gw_category'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Category.objects.create(
			name =		v['name'],
			user_id =	pk_cache.get('auth_user', int(v['user_id'])) if v['user_id'] else None,
			app_id =	pk_cache.get('django_content_type', int(v['app_id'])) if v['app_id'] else None,
			description =	v['description']
		).pk)
	# 1
	modelname = 'gw_vevent'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], vEvent.objects.create(
			user_id =	pk_cache.get('auth_user', int(v['user_id'])) if v['user_id'] else None,
			created =	v['created'],
			updated =	v['updated'],
			summary =	v['summary'],
			status =	v['status'],
			restriction =	v['restriction'],
			attendee_id =	pk_cache.get('auth_user', int(v['attendee_id'])) if 'attendee_id' in v else None,
			description =	v.get('description', None),
			start_d =	v.get('start_d', None),
			start_t =	v.get('start_t', None),
			duration_d =	v.get('duration_d', None),
			duration_t =	v.get('duration_t', None),
			location =	v.get('location', None),
			priority =	v.get('priority', None),
			URL =		v.get('URL', None),
			end_d =		v.get('end_d', None),
			end_t =		v.get('end_t', None),
		).pk)
	# 2
	modelname = 'gw_vtodo'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		item = vToDo(
			user_id =	pk_cache.get('auth_user', int(v['user_id'])) if v['user_id'] else None,
			created =	v['created'],
			updated =	v['updated'],
			summary =	v['summary'],
			status =	v['status'],
			restriction =	v['restriction'],
			attendee_id =	pk_cache.get('auth_user', int(v['attendee_id'])) if 'attendee_id' in v else None,
			description =	v.get('description', None),
			start_d =	v.get('start_d', None),
			start_t =	v.get('start_t', None),
			duration_d =	v.get('duration_d', None),
			duration_t =	v.get('duration_t', None),
			location =	v.get('location', None),
			priority =	v.get('priority', None),
			URL =		v.get('URL', None),
			due_d =		v.get('due_d', None),
			due_t =		v.get('due_t', None),
			completed =	v.get('completed', None),
			percent =	v.get('percent', None)
		)
		item.raw_save()		# w/o logging
		pk_cache.set(modelname, i[0], item.pk)
	# 5. Task
	pk_cache.copy('gw_task', 'gw_vevent')
	pk_cache.copy('gw_task', 'gw_vtodo')
	# 4. Task.Category
	modelname = 'gw_taskcat'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		TaskCat.objects.create(
			task_id =	pk_cache.get('gw_task', long(v['task_id'])),
			cat_id =	pk_cache.get('gw_category', long(v['cat_id']))
		)
	reset_queries()

@transaction.commit_on_success
def	contact():
	global db, pk_cache
	# 0. Person
	modelname = 'gw_person'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Person.objects.create(
			firstname =	v['firstname'],
			midname =	v['midname'],
			lastname =	v['lastname'],
			birthdate =	v['birthdate'],
			sex =		v['sex']
		).pk)
	# 1. Org
	modelname = 'gw_org'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Org.objects.create(
			user_id =	pk_cache.get('auth_user', int(v['user_id'])) if v['user_id'] else None,
			name =		v['name'],
			shortname =	v['shortname'],
			fullname =	v['fullname'],
			brandname =	v['brandname'],
			egruldate =	v['egruldate'],
			inn =		v['inn'],
			kpp =		v['kpp'],
			ogrn =		v['ogrn'],
			okato_id =	v['okato_id'],
			okopf_id =	v['okopf_id'],
			comments =	v['comments']
		).pk)
	# 2. OrgOkved
	modelname = 'gw_orgokved'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		OrgOkved.objects.create(
			org_id =	pk_cache.get('gw_org', int(v['org_id'])),
			okved_id =	pk_cache.get('ref_okved', int(v['okved_id']))
		)
	# 3. JobRole
	modelname = 'gw_jobrole'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], JobRole.objects.create(
			name =		v['name'],
			comments =	v['comments']
		).pk)
	# 4. OrgStuff
	modelname = 'gw_orgstuff'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		JobRole.objects.create(
			org_id =	pk_cache.get('gw_org', int(v['org_id'])),
			role_id =	pk_cache.get('gw_jobrole', int(v['role_id'])),
			person_id =	pk_cache.get('gw_person', int(v['person_id']))
		)
	# 5. Contact
	pk_cache.copy('gw_contact', 'gw_person')
	pk_cache.copy('gw_contact', 'gw_org')
	# 6. ContactAddrType
	modelname = 'gw_contactaddrtype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], ContactAddrType.objects.create(
			id =	i[0],
			name =	v['name']
		).pk)
	# 7. ContactAddr
	modelname = 'gw_contactaddr'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], ContactAddr.objects.create(
			contact_id =	pk_cache.get('gw_contact', int(v['contact_id'])),
			addr_id =	pk_cache.get('gw_address', int(v['address_id']))
		).pk)
	# 8. Contact2AddrType
	modelname = 'gw_contact2addrtype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], Contact2AddrType.objects.create(
			caddr_id =	pk_cache.get('gw_contact', int(v['caddr_id'])),
			type_id =	pk_cache.get('gw_contactaddrtype', int(v['type_id']))
		).pk)
	# 9. ContactPhone
	modelname = 'gw_contactphone'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		ContactPhone.objects.create(
			contact_id =	pk_cache.get('gw_contact', int(v['contact_id'])),
			phone_id =	pk_cache.get('gw_phone', int(v['phone_id'])),
			ext =		v['ext']
		)
	# 10. ContactWWW
	modelname = 'gw_contactwww'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		ContactWWW.objects.create(
			contact_id =	pk_cache.get('gw_contact', int(v['contact_id'])),
			www_id =	pk_cache.get('gw_www', int(v['www_id']))
		)
	# 11. ContactEmail
	modelname = 'gw_contactemail'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		ContactWWW.objects.create(
			contact_id =	pk_cache.get('gw_contact', int(v['contact_id'])),
			email_id =	pk_cache.get('gw_email', int(v['email_id']))
		)
	# 12. ContactIM
	modelname = 'gw_contactim'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		ContactIM.objects.create(
			contact_id =	pk_cache.get('gw_contact', int(v['contact_id'])),
			im_id =		pk_cache.get('gw_im', int(v['im_id']))
		)
	reset_queries()

#@transaction.commit_on_success
def	file():
	'''
	WARNING: delete all files from MEDIA
	Algo:
		* create zero file w/ old id
		* create record
		* rename file to new id
		* resave record
		* print old=>new filename
	'''
	global db, pk_cache
	# 0
	modelname = 'gw_imagefile'
	log(modelname)
	file = open("file.lst", "w+")
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		# 1. create fake file w/ old name
		old_fn = v['file']
		open(os.path.join(MEDIA_ROOT, old_fn), "w+").close()
		# 2. save record w/ old file name (renaming automaticaly)
		item = ImageFile(
			file = old_fn,
			name = v['name'],
			mime = v['mime'],
			saved = v['saved'],
			size = v['size'],
			md5 = v['md5'],
			width = v['width'],
			height = v['height'],
			pages = v['pages']
		)
		item.raw_save()
		new_fn = "%08d" % item.pk
		pk_cache.set(modelname, i[0], item.pk)
		file.write("%s\t%s\n" % (old_fn, new_fn))
	reset_queries()
	pk_cache.copy('gw_file', 'gw_imagefile')
	pk_cache.copy('gw_object', 'gw_file')

@transaction.commit_on_success
def	tagged():
	global db, pk_cache, ct_cache
	# 0. TaggedObjectType
	modelname = 'gw_taggedobjecttype'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], TaggedObjectType.objects.create(
			name =		v['name'],
			comments =	v['comments']
		).pk)
	# 1. TaggedObjectTagType
	modelname = 'gw_taggedobjecttagtype'
	log(modelname)
	tott = dict()	# dict of tag types
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_options = v['options'] if (v['type'] != 4) else str(pk_cache.get('django_content_type', int(v['options'])))
		new_id = TaggedObjectTagType.objects.create(
			name =		v['name'],
			tot_id =	pk_cache.get('gw_taggedobjecttype', int(v['tot_id'])),
			type =		v['type'],
			multiplicity =	v['multiplicity'],
			options =	new_options
		).pk
		pk_cache.set(modelname, i[0], new_id)
		tott[new_id] = (int(v['type']), new_options)	# ? int(v['type'] ?
	# 2. TaggedObject
	modelname = 'gw_taggedobject'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], TaggedObject.objects.create(
			object_id =	pk_cache.get('gw_object', i[0]),
			tot_id =	pk_cache.get('gw_taggedobjecttype', int(v['tot_id']))
		).pk)
	# 3. TaggedObjectTag
	# value: if type.type = 4, then type.options == ContentType + value = object.pk
	modelname = 'gw_taggedobjecttag'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_type_id = pk_cache.get('gw_taggedobjecttagtype', int(v['type_id']))
		if tott[new_type_id][0] == 4:
			new_ct_id = tott[new_type_id][1]
			new_ct = ct_cache[new_ct_id]
			#model_name = new_ct.app_label + '_' + new_ct.model	# FIXME: get from RAM
			model_name = new_ct.db_table
			new_value = pk_cache.get(model_name, v['value'])
		else:
			new_value = v['value']
		pk_cache.set(modelname, i[0], TaggedObjectTag.objects.create(
			object_id =	pk_cache.get('gw_taggedobject', long(v['object_id'])),
			type_id =	new_type_id,
			value =		new_value	# !!! FIXME: !!!
		).pk)
	reset_queries()
	pk_cache.copy('gw_object', 'gw_taggedobjecttag')

@transaction.commit_on_success
def	objectlinks():
	global db, pk_cache
	# 0. ObjectLink
	modelname = 'gw_objectlink'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		pk_cache.set(modelname, i[0], ObjectLink.objects.create(
			left_id =	pk_cache.get('gw_object', long(v['left'])),
			right_id =	pk_cache.get('gw_object', long(v['right']))
		).pk)
	reset_queries()
	pk_cache.copy('gw_object', modelname)

@transaction.commit_on_success
def	logentry():
	'''
	LogEntry (django_admin_log)
	LogEntryField (gw_logentry)
	Algo:
		LogEntry:
			* get content type
			* get new CT
			* get new pk
		LogEntryField:
			* if pk - ...
			* if FK or 121 - get CT of FK (FK.to_field, 
	'''
	global db, pk_cache, ct_cache
	# 0. LogEntry
	modelname = 'django_admin_log'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_ct_id = pk_cache.get('django_content_type', int(v['content_type_id']))
		if (new_ct_id != None):
			new_ct = ct_cache[new_ct_id]
			new_object_id = pk_cache.get(new_ct.model_class()._meta.db_table, long(v['object_id']))
			if (new_object_id != None):
				pk_cache.set(modelname, i[0], LogEntry.objects.create(
					user_id =		pk_cache.get('auth_user', int(v['user_id'])),
					content_type_id =	new_ct_id,
					object_id =		new_object_id,
					object_repr =		v['object_repr'],
					action_flag =		v['action_flag'],
					change_message =	v['change_message']
				).pk)
	# 1. LogEntryField
	modelname = 'gw_logentryfield'
	log(modelname)
	# 1.1. create models cache: [ct_id: [fieldname: fk:bool] ]
	model_cache = dict()
	for ct_id, ct in ct_cache.iteritems():
		model_cache[ct_id] = dict()
		for field in ct.model_class()._meta.fields:
			model_cache[ct_id][field.name] = (isinstance(field, models.ForeignKey) or isinstance(field, models.OneToOneField))
	# 1.2. lets go
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_logentry_id = pk_cache.get('django_admin_log', int(v['logentry_id']))
		if (new_logentry_id != None):
			logentry = LogEntry.objects.get(pk=new_logentry_id)	# FIXME: cache it
			model = ct_cache[logentry.content_type_id].model_class()
			towrite = True
			if (model_cache[logentry.content_type_id][v['field']]):
				if (v['value']):
					value = pk_cache.get(ct_cache[logentry.content_type_id].db_name, long(v['value']))
					towrite = (value != None)
			else:
				value = v['value']
			if (towrite):
				pk_cache.set(modelname, i[0], LogEntryField.objects.create(
					logentry_id =	new_logentry_id,
					field =		v['field'],
					value =		value
				).pk)
	reset_queries()

@transaction.commit_on_success
def	permissions():
	'''
	'''
	global db, pk_cache, ct_cache
	# 0. UserPermission
	modelname = 'objectpermissions_userpermission'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_ct_id = pk_cache.get('django_content_type', int(v['content_type_id']))
		if (new_ct_id != None):
			new_ct = ct_cache[new_ct_id]
			new_object_id = pk_cache.get(new_ct.db_table, long(v['object_id']))
			if (new_object_id != None):
				pk_cache.set(modelname, i[0], UserPermission.objects.create(
					user_id =		pk_cache.get('auth_user', int(v['user_id'])),
					content_type_id =	new_ct_id,
					object_id =		new_object_id,
					permission =		v['permission']
				).pk)
	# 1. GroupPermission
	modelname = 'objectpermissions_grouppermission'
	log(modelname)
	for i in (db.get_idlist(modelname)):
		v = db.get_fields(modelname, i[0])
		new_ct_id = pk_cache.get('django_content_type', int(v['content_type_id']))
		if (new_ct_id != None):
			new_ct = ct_cache[new_ct_id]
			new_object_id = pk_cache.get(new_ct.db_table, long(v['object_id']))
			if (new_object_id != None):
				pk_cache.set(modelname, i[0], GroupPermission.objects.create(
					group_id =		pk_cache.get('auth_group', int(v['group_id'])),
					content_type_id =	new_ct_id,
					object_id =		new_object_id,
					permission =		v['permission']
				).pk)
	reset_queries()

def	main(dbname):
	global db, pk_cache
	db = SqliteStorage()
	db.init(dbname)
	pk_cache = CacheRAM()
	ct()		# 0.1. sync CT: id, app_label:str, model:str
	# 2. user, auth_*, django_*
	auth()
	# <test>
	#return
	# </test>
	# 3. ref
	okato()
	okopf()
	oksm()
	okved()
	kladr()		# after okato
	# phonecountry
	# phonetrunk
	# UserSettings - skip
	address()
	phone()
	www()
	email()
	im()
	task()		# after user
	contact()	# after address
	file()
	tagged()
	objectlinks()
	permissions()
	logentry()
	# X. the end

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <sqlite.db>" % sys.argv[0]
		exit(0)
	main(sys.argv[1])
	log("The End")
