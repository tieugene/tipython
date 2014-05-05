#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Converts data from 0.0.3 to 0.1.0
Src:
* ./manage.py dumpdata --format=json --indent=1 -a > 0.0.3.json
Dst:
* ./03_10.py 0.0.3.json > 0.1.0.json
* ./manage.py syncdb
* ./manage.py loaddata 0.1.0.json
* ./manage.py syncdb

Handle:
-- del record
-- modify record:
--- del attr
--- rename attr
-- add record
'''

import sys, json, pprint

'''
18/23:
MODIFY:
	bills.route:
		-state
		-action
	bills.bill:
		-project
		+place = addon.place
		+subject = addon.subject
		+depart = addon.depart
		+payer		= null
		+billdate	= 01.01.1970
		+billno		= '-'
		+billsum	= 0
		+payedsum	= 0
		+topaysum	= 0
CP:
	?admin.logentry
	?auth.group
	?auth.permission
	?contenttypes.contenttype
	?sessions.session
	?sites.site
	auth.user
	core.file
	core.fileseq
	core.fileseqitem
	bills.approver
	bills.role
	bills.event (.comment: text => char)
	scan.scan
	scan.event
RENAME:
	bills.place = addon.place
	bills.subject = addon.subject
	bills.depart = addon.depart
	bills.payer = addon.payer
TODEL:
	addon.addon
	?bills.state
'''

ADDON = dict()	# bill.pk: place, subject, depart
MODELS = set()
TORENAME = {
	'addon.department':	'bills.department',
	'addon.payer':		'bills.payer',
	'addon.place':		'bills.place',
	'addon.subject':	'bills.subject',
}
TOSKIP = set([
	'addon.addon',
])

def	bills_event(rec):
	return {
		'pk': rec['pk'],
		'model': rec['model'],
		'fields': {
		}
	}

def	bills_route(rec):
	return {
		'pk': rec['pk'],
		'model': rec['model'],
		'fields': {
			'bill':		rec['fields']['bill'],
			'role':		rec['fields']['role'],
			'approve':	rec['fields']['approve'],
			'order':	rec['fields']['order']
		}
	}

def	bills_bill(rec):
	pk = rec['pk']
	addon = ADDON.get(pk, None)
	if addon:
		return {
			'pk': rec['pk'],
			'model': rec['model'],
			'fields': {
				'fileseq':	rec['fields']['fileseq'],
				'rpoint':	rec['fields']['rpoint'],
				#'project': rec['fields'][''],
				'done':		rec['fields']['done'],
				'supplier':	rec['fields']['supplier'],
				'assign':	rec['fields']['assign'],
				'place':	addon['place'],
				'subject':	addon['subject'],
				'depart':	addon['depart'],
				'payer':	None,
				'billdate':	'1970-01-01',
				'billno':	'-',
				'billsum':	0,
				'payedsum':	0,
				'topaysum':	0,
			}
		}

TOMODIFY = {
	#'bills.event':	bills_event,
	'bills.route':	bills_route,
	'bills.bill':	bills_bill,
}

def	main(infile):
	result = list()
	data = json.load(open(infile))
	# 1. preload some data
	for rec in data:
		model = rec['model']
		#if not model in MODELS:
		#	MODELS.add(model)
		# 1.1. rename
		if model in TORENAME:
			rec['model'] = TORENAME[model]
		# 1.2. preload
		elif model == u'addon.addon':
			ADDON[rec['pk']] = rec['fields']
	# 2. go
	for rec in data:
		model = rec['model']
		if model in TOSKIP:
			continue
		elif model in TOMODIFY:
			newrec = TOMODIFY[model](rec)
			if newrec:
				result.append(newrec)
		else:
			result.append(rec)
	#pprint.pprint(MODELS)
	print json.dumps(result, indent=1, encoding='utf-8')

if __name__ == '__main__':
	main(sys.argv[1])
