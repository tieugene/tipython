#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Stage #1: SQL2sqlite_plain - script to convert sql dump into plain sqlite db.
Test:
	1M lines:
		time:
			wc-l:		10"
			parse:		233"
			w/o commit:	15' == 900"
			w/ commit:	17'51", 308M
	5129923 lines:
		time:	50"
		indices:	8"
		size:	1383M (250M gzipped)
		recs:	17555132
'''

import os, sys, gzip, re, sqlite3, datetime, pprint
from odict import OrderedDict
#from meminfo import getusedmem

inttype = type(1)
longtype = type(1L)
strtype = type('str')

r = (
	re.compile('^INSERT INTO `(\w+)` \(([^\)]+)\) VALUES \((.+)\);$'),	# 1. split to tablename | filednames | fieldvalues
	re.compile('`([0-9A-Za-z_]+)`'),					# 2. fieldnames
	re.compile('''([0-9]+)|'((?:[^'\\\\]|\\\\.)*)'|(NULL)'''),		# 3. fieldvalues
)

reload(sys)
sys.setdefaultencoding("utf-8")

def	now():
	return datetime.datetime.now().strftime("%H:%M:%S")

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
			if (m.group(1) == 'django_session'):
				return (True, None)			# skip django_session
			result = (m.group(1), OrderedDict())		# (table, {fieldname = > fieldvalue}
			for i, v in enumerate(values):
				if v[2]:
					result[1][fields[i]] = 'NULL'		# was None
				elif v[0]:
					result[1][fields[i]] = v[0]		# was long(v[0])
				else:
					result[1][fields[i]] = u'\'%s\'' % v[1].replace("'", "''")	# !!!; was v[1]
			return (True, result)
		else:
			print >> sys.stderr, u'ERROR in line %d: Table:' % n, m.group(1), ", Fields (%d):" % len(fields), m.group(2), "=>", fields, ", Values (%d):" % len(values), m.group(3), "=>", values
			return (False, None)
	else:
		print >> sys.stderr, u'ERROR in line %d: It\'s not SQL string: %s' % (n, s)
		print >> sys.stderr, s
		return (False, None)

class	SqliteStorage:
	def	__init__(self):
		self.con = None
		self.cur = None
	def	init(self):
		self.con = sqlite3.connect('data.db')
		self.cur = self.con.cursor()
		self.cur.execute('''CREATE TABLE data (model VARCHAR(20) NOT NULL, record INTEGER NOT NULL, field VARCHAR(20) NOT NULL, value VARCHAR(255));''')
		self.con.commit()
	def	add(self, q, r):
		'''
		Insert new fild bulk
		'''
		# 1. record
		r_id = None
		for i in r[1].keys():
			if (
				(i == 'id') or
				(i.endswith('_ptr_id')) or
				((r[0] == 'gw_taggedobject') and (i == 'object_id')) or
				((r[0] == 'ref_kladrokato') and (i == 'kladr_id'))
			):
				r_id = long(r[1][i])
				del r[1][i]
				break;
		if r_id == None:
			print >> sys.stderr, "Can't find pk at line %d:" % q
			pprint.pprint(r)
			#exit(1)
			return False
		# 3. fields
		for n, v in r[1].items():
			try:
				#self.cur.execute("INSERT INTO data (model, record, field, value) VALUES ('%s', %d, '%s', %s);" % (r[0], r_id, n, v))
				self.cur.execute("INSERT INTO data (model, record, field, value) VALUES (?, ?, ?, ?);" % (r[0], r_id, n, v))
			except:
				print >> sys.stderr, "INSERT INTO data (model, record, field, value) VALUES ('%s', %d, '%s', %s);" % (r[0], r_id, n, v)
		return True

	def	commit(self):
		self.con.commit()

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <gzipeddumpfile>" % sys.argv[0]
		exit(0)
	file = gzip.open(sys.argv[1], 'r')
	if not file:
		print >> sys.stderr, u'ERROR: can\'t open dump'
		exit(1)
	mydb = SqliteStorage()
	mydb.init()
	print >> sys.stderr, now(), "Start"
	for q, s in enumerate(file):
		ok, result = splitsql(q, s)
		if ok:
			if (result != None):
				#print >> sys.stderr, q
				mydb.add(q, result)
		else:
			print >> sys.stderr, u'ERROR: can\'t parse line %d' % q
			#exit(2)
		#if q > 1000000:
		#	break
		if (q % 1000000 == 999999):
			print >> sys.stderr, now(), "Commiting %d" % (q + 1)
			mydb.commit()
	file.close()
	print >> sys.stderr, now(), "To flush"
	mydb.commit()
	print >> sys.stderr, now(), "Create indises"
	mydb.cur.execute('''CREATE INDEX model ON data (model);''')
	mydb.cur.execute('''CREATE INDEX record ON data (record);''')
	mydb.cur.execute('''CREATE INDEX field ON data (field);''')
	mydb.cur.execute('''CREATE INDEX value ON data (value);''')
	mydb.commit()
	print >> sys.stderr, now(), "The End"
