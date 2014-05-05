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
	bills.event:
		- .comment: text => char
	bills.route:
		-state
		-action
	bills.bill:
		?project
		+place = addon.addon.place
		+subject = addon.addon.subject
		+depart = addon.addon.depart
		+payer		= None
		+billdate	= 01.01.1970
		+billno		= '-'
		+billsum	= 0
		+payedsum	= 0
		+topaysum	= 0
	scan.scan:
	scan.event: json it
CP:
	?admin.logentry
	?auth.group
	?auth.permission
	?bills.state
	?contenttypes.contenttype
	?sessions.session
	?sites.site
	auth.user
	core.file
	core.fileseq
	core.fileseqitem
	bills.approver
	bills.role
RENAME:
	bills.place = addon.place
	bills.subject = addon.subject
	bill.depart = addon.depart
	bills.payer = addon.payer
TODEL:
	addon.addon
	?scan.event
'''

TORENAME = {
	'addon.department':	'bills.department',
	'addon.payer':		'bills.payer',
	'addon.place':		'bills.place',
	'addon.subject':	'bills.subject',
}

ADDON = dict()	# bill.pk: place, subject, depart
SCAN_EVENT = dict()	# bill.pk: {}
MODELS = set()
RESULT = list()

def	main(infile):
	result = list()
	data = json.load(open(infile))
	# 1. preload some data
	for rec in data:
		model = rec['model']
		#if rec['model'] in TOINIT:
		#	result.append(rec)
		if not model in MODELS:
			MODELS.add(model)
		# 1.1. rename
		if model in TORENAME:
			rec['model'] = TORENAME[model]
		# 1.2. preload
		#if rec['model'] == u'scan.event':
		#	SCAN_EVENT[rec['field']['scan']] = ...
		elif model == u'addon.addon':
			ADDON[rec['pk'] = rec['fields']
	# 2. go
	for rec in data:
		pass
	pprint.pprint(MODELS)
	#print json.dumps(result, indent=1, encoding="utf-8")

if __name__ == '__main__':
	main(sys.argv[1])
