#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
SQL2json - script to convert sql dump into json.
Usage:
	* $0 gzippeddump > new.sql 2>new.err
Contrib:
	http://code.activestate.com/recipes/475109-regular-expression-for-python-string-literals/
	http://docs.python.org/release/2.4/lib/re-syntax.html
	http://www.regular-expressions.info/lookaround.html
Test:
	data.sql[.gz] - 4140616 lines
	10k lines:	6"	23M
	100k lines:	43"	223M
	500k lines:	215"	1086M (500M on json)
'''

import os, sys, gzip, re, json, pprint
from odict import OrderedDict
from meminfo import getusedmem

r = (
	re.compile('^INSERT INTO `(\w+)` \(([^\)]+)\) VALUES \((.+)\);$'),	# 1. split to tablename | filednames | fieldvalues
	re.compile('`([0-9A-Za-z_]+)`'),					# 2. fieldnames
	re.compile('''([0-9]+)|'((?:[^'\\\\]|\\\\.)*)'|(NULL)'''),		# 3. fieldvalues
)

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

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <gzipeddumpfile> > <outputjson>" % sys.argv[0]
		exit(0)
	data = list()
	print >> sys.stderr, "Start:", getusedmem()
	file = gzip.open(sys.argv[1], 'r')
	if not file:
		print >> sys.stderr, u'ERROR: can\'t open dump'
		exit()
	for q, s in enumerate(file):
		ok, result = splitsql(q, s)
		if ok:
			data.append(result)
		if q > 500000:
			break
	file.close()
	print >> sys.stderr, "End process file:", getusedmem()
	print json.dumps(data, indent=1)
	print >> sys.stderr, "The end:", getusedmem()
