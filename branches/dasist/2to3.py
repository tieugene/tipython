#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Converts data from 0.0.2 to 0.0.3
* load json
* handle:
-- del record
-- modify record:
--- del attr
--- rename attr
-- add record
* save json
'''

import sys, json

'''
TODEL:
admin.logentry
auth.group
auth.permission
contenttypes.contenttype
sessions.session
sites.site
bills.state
bills.bill (pk)
bills.event
bills.route (-state, -action)

TOINIT:
auth.user
bills.approver
bills.role

TOSAVE:
core.file
core.fileseq
core.fileseqitem - pk
scan.event - tojson
scan.scan  - +comments field
'''

TOINIT=set([
'auth.user',
'bills.approver',
'bills.role',
])

def	main(infile):
	result = list()
	data = json.load(open(infile))
	for rec in data:
		if rec['model'] in TOINIT:
			result.append(rec)
	print json.dumps(result, indent=1, encoding="utf-8")

if __name__ == '__main__':
	main(sys.argv[1])
