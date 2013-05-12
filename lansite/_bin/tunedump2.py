#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TuneDump - script to prepare dump for restoring.
Usage:
	* $0 gzippeddump > new.sql 2>new.err
Main features:
	* remove unwanted lines
	* change FKs to django_content_type
	* change FKs to auth_permission
What remove:
	* auth_permission (AP)
	* django_content_type (CT)
	* django_site
Who to tune:
	* CT:
		* *.content_type_id <= content_type_id (AND kill id !!!)
		* *.polymorphic_ctype_id <= content_type_id
	* AP:
		* auth_group_permissions.permission_id <= auth_permission.id
		* auth_user_user_permissions.permission_id <= auth_permission.id
	* etc:
		* del django_admin_log.id
Contrib:
	http://code.activestate.com/recipes/475109-regular-expression-for-python-string-literals/
	http://docs.python.org/release/2.4/lib/re-syntax.html
	http://www.regular-expressions.info/lookaround.html
'''

REQ = {'db': 'sro2', 'user': 'lansite', 'password': 'lansite'}	# db, login, password

import os, sys, gzip, re, MySQLdb, pprint
from odict import OrderedDict

r = (
	re.compile('^INSERT INTO `(\w+)` \(([^\)]+)\) VALUES \((.+)\);$'),	# 1. split to tablename | filednames | fieldvalues
	re.compile('`([0-9A-Za-z_]+)`'),					# 2. fieldnames
	re.compile('''([0-9]+)|'((?:[^'\\\\]|\\\\.)*)'|(NULL)'''),			# 3. fieldvalues
)
#(?:[^']\\')*'(?!')
	#re.compile('([0-9]+)|\'([^\']*)\'|(NULL)'),				# 3. fieldvalues

inttype = type(1)
longtype = type(1L)
strtype = type('str')

reload(sys)
sys.setdefaultencoding("utf-8")

def	splitsql(n, s):
	'''
	Splits SQL string to (table, {fieldnames: fieldvalues})
	@param n:int - string number
	@param s:str - SQL string
	@return bool, (tablename:str, {fieldnames: fieldvalues})
	'''
	m = r[0].match(s)
	if m:
		fields = r[1].findall(m.group(2))			# list of str
		values = r[2].findall(m.group(3))			# list of tuples
		if (len(fields) != 0) and (len(fields) == len(values)):
			result = (m.group(1), OrderedDict())		# (table, {fieldname = > fieldvalue}
			for i, v in enumerate(values):
				if v[2]:
					result[1][fields[i]] = None
				elif v[0]:
					result[1][fields[i]] = long(v[0])
				else:
					result[1][fields[i]] = v[1]
			return (True, result)
		else:
			print >> sys.stderr, u'ERROR in line %d: Table:' % n, m.group(1), ", Fields (%d):" % len(fields), m.group(2), "=>", fields, ", Values (%d):" % len(values), m.group(3), "=>", values
			return (False, None)
	else:
		print >> sys.stderr, u'ERROR in line %d: It\'s not SQL string' % n
		return (False, None)

def	vtostr(v):
	'''
	Convert v into string for mysql
	'''
	if v is None:
		return 'NULL'
	elif type(v) == inttype:
		return str(v)
	elif type(v) == longtype:
		return str(v)
	return "'" + v + "'"

def	mergesql(l):
	'''
	Merges splitted SQL into SQL string
	@param l:tuple - (table, {fieldnames: fieldvalues})
	'''
	return "INSERT INTO `%s` (`%s`) VALUES (%s);" % (l[0], '`, `'.join(l[1].keys()), ','.join(map(vtostr, l[1].values())))

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <gzipeddumpfile>" % sys.argv[0]
		exit(0)
	# 0. get current data from DB
	ct_dict_0 = dict()	# index of ct: app+model => new id
	ct_dict_1 = dict()	# index of ct: old id => new id
	ap_dict_0 = dict()	# index of ap: codename => new id
	ap_dict_1 = dict()	# index of ap: old id => new id
	sysapps = set(('admin', 'auth', 'contenttypes', 'sessions', 'sites'))				# CTs to not handle !!! be carefull !!!
	db = MySQLdb.connect(user=REQ['user'], passwd=REQ['password'], db=REQ['db'])
	c = db.cursor()
	# 0.1. CTs
	c.execute('SELECT id, app_label, model FROM django_content_type ORDER BY id')
	for rec in c.fetchall():
		if rec[1] not in sysapps:								# user apps only
			ct_dict_0[(rec[1], rec[2])] = int(rec[0])					# from long
	#pprint.pprint(ct_dict_0)
	# 0.2. permissions
	c.execute('SELECT id, codename FROM auth_permission ORDER BY id')				# ?content_type_id?
	for rec in c.fetchall():
		ap_dict_0[rec[1]] = int(rec[0])								# from long
	# 0.x that's all
	db.close()
	# 1. get old data from dump and make translation tables
	file = gzip.open(sys.argv[1], 'r')
	if not file:
		print >> sys.stderr, u'ERROR: can\'t open dump'
		exit()
	ct_done = False		# flag to end filling out contenttypes: 0 - not started, 1 - started, 2 - filled out
	ap_done = False		# flag to end filling out contenttypes: 0 - not started, 1 - started, 2 - filled out
	for q, s in enumerate(file):
		ok, result = splitsql(q, s)
		if ok:
			if result[0] == 'django_content_type':
				if not ct_done:
					ct_done = True	# starting ct
				if result[1]['app_label'] not in sysapps:
					key = (result[1]['app_label'], result[1]['model'])
					newid = ct_dict_0.get(key)
					if newid:
						ct_dict_1[result[1]['id']] = newid
					else:
						print >> sys.stderr, u'ERROR line %d: can\'t find new id for CT (%s, %s)' % (0,q, key)
						exit()
			elif result[0] == 'auth_permission':
				if not ap_done:
					ap_done = True		# starting ct
				key = result[1]['codename']
				newid = ap_dict_0.get(key)
				if newid:
					ap_dict_1[result[1]['id']] = newid
				else:
					print >> sys.stderr, u'ERROR line %d: can\'t find new id for AP (%s)' % (q, key)
					#exit()
			else:					# not interesting - time to stop?
				if ct_done and ap_done:		# ct & ap was filled
					break
		else:
			exit()
		#if q > 100000:
		#	break
	#pprint.pprint(ct_dict_1)
	#pprint.pprint(ap_dict_1)
	#exit()
	file.seek(0)
	# stage 2: sync dump's AP w/ dump's CT
	# stage 3: parse
	toskip = set(('auth_permission', 'django_content_type', 'django_site', 'django_session'))	# tables to skip in new dump
	permset = set(('auth_group_permissions', 'auth_user_user_permissions'))
	for q, s in enumerate(file):
		ok, result = splitsql(q, s)
		if ok:
			if result[0] not in toskip:
				if result[0] in permset:
					key = result[1]['permission_id']
					if ap_dict_1.has_key(key):
						result[1]['permission_id'] = ap_dict_1[key]
					else:
						print >> sys.stderr, u'WARNING line %d: key %s skipped' % (q, key)
				else:
					# ====
					if result[0] == 'django_admin_log':
						del result[1]['id']
					ctname = 'content_type_id'
					if result[1].has_key(ctname):
						ct = result[1][ctname]
						if (ct_dict_1.has_key(ct)):
							result[1][ctname] = ct_dict_1[ct]
						else:
							print >> sys.stderr, u'WARNING line %d: can\'t ct: %s' % (q, mergesql(result))
					ctname = 'polymorphic_ctype_id'
					if result[1].has_key(ctname):
						ct = result[1][ctname]
						if (ct_dict_1.has_key(ct)):
							result[1][ctname] = ct_dict_1[ct]
						else:
							print >> sys.stderr, u'WARNING line %d: can\'t ct: %s' % (q, mergesql(result))
					print mergesql(result)
	file.close()
