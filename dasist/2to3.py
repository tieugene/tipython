#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Converts data from 0.0.2 to 0.0.3
Src:
* ./manage.py dumpdata --format=json --indent=1 -a > 0.0.3.json
Dst:
* load json
* handle:
-- del record
-- modify record:
--- del attr
--- rename attr
-- add record
* save json
'''

import sys, json, pprint

'''
18/23:
DEL:
	admin.logentry
	auth.group
	auth.permission
	bills.state
	contenttypes.contenttype
	sessions.session
	sites.site
CP:
	auth.user
	core.file
	core.fileseq
	core.fileseqitem
	bills.approver
	bills.role
ADD:
	bills.place
	bills.subject
	bills.payer
MODIFY:
	bills.event:
		- .comment => char
	bills.route:
		-state
		-action
	bills.bill:
		?project
		+place
		+subject
		+payer		= 1
		+billdate	= 01.01.1970
		+billno		= '-'
		+billsum	= 0
		+payedsum	= 0
		+topaysum	= 0
	scan.scan:
	scan.event: json it
'''

TOINIT=set([
	'auth.user',
	'bills.approver',
	'bills.role',
])

MODELS = set()

def	main(infile):
	result = list()
	data = json.load(open(infile))
	for rec in data:
		#if rec['model'] in TOINIT:
		#	result.append(rec)
		if not rec['model'] in MODELS:
			MODELS.add(rec['model'])
	pprint.pprint(MODELS)
	#print json.dumps(result, indent=1, encoding="utf-8")

if __name__ == '__main__':
	main(sys.argv[1])
