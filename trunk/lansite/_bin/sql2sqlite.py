#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
SQL2sqlite - script to convert sql dump into json.
pk can be named:
	id
	*_ptr_id
Test:
	10k lines:
		3xCommits per rec: 5'30" (30/s) => 2.3 days
		1xCommits per rec: 3'34" (46/s) => 1.5 days
		1xCommit per db: 10" (1k/s) => 1:40:00 (2.5M, dbsize=6M)
	100k lines:
		time: 1'42" (100s)
		RAM: 17M
		DB: 22.6M
	100k lines, :memory::
		time: 1'31" (90s)
		RAM: 27M
	1M lines:
		time: 16' ()
		time w/o db: 3'30"
		DB: 230M
'''

import os, sys, gzip, re, sqlite3, pprint
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

sql = (
	'''CREATE TABLE m (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20) UNIQUE );''',
	'''CREATE TABLE r (m_id REFERENCES m(id), id INTEGER);''',
	'''CREATE TABLE f (r_id REFERENCES r(id), name VARCHAR(20) NOT NULL, value VARCHAR(255));''',
)

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
					result[1][fields[i]] = 'NULL'		# was None
				elif v[0]:
					result[1][fields[i]] = v[0]		# was long(v[0])
				else:
					result[1][fields[i]] = u'"%s"' % v[1]	# was v[1]
			return (True, result)
		else:
			print >> sys.stderr, u'ERROR in line %d: Table:' % n, m.group(1), ", Fields (%d):" % len(fields), m.group(2), "=>", fields, ", Values (%d):" % len(values), m.group(3), "=>", values
			return (False, None)
	else:
		print >> sys.stderr, u'ERROR in line %d: It\'s not SQL string' % n
		return (False, None)

class	SqliteStorage:
	def	__init__(self):
		self.con = None
		self.cur = None
		self.m = dict()
	def	init(self):
		self.con = sqlite3.connect('data.db')
		self.cur = self.con.cursor()
		self.cur.execute(sql[0])	# model
		self.cur.execute(sql[1])
		self.cur.execute(sql[2])
		self.con.commit()
	def	add(self, q, r):
		'''
		Insert new fild bulk
		'''
		# 1. model
		m_name = r[0]
		if m_name in self.m:
			m_id = self.m[m_name]
		else:
			self.cur.execute("INSERT INTO m (name) VALUES ('%s');" % m_name)
			#self.con.commit()
			m_id = self.cur.lastrowid
			self.m[m_name] = m_id
		# 2. record
		r_id = None
		for i in r[1].keys():
			if (i == 'id' or i.endswith('_ptr_id')):
				r_id = long(r[1][i])
				del r[1][i]
				self.cur.execute("INSERT INTO r (m_id, id) VALUES (%d, %d);" % (m_id, r_id))
				#self.con.commit()
				break;
		if r_id == None:
			print >> sys.stderr, "Can't find pk"
			return False
		# 3. fields
		for n, v in r[1].items():
			self.cur.execute("INSERT INTO f (r_id, name, value) VALUES (%d, '%s', %s);" % (r_id, n, v))
		return True
	def	commit(self):
		self.con.commit()

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <gzipeddumpfile> > <outputjson>" % sys.argv[0]
		exit(0)
	file = gzip.open(sys.argv[1], 'r')
	if not file:
		print >> sys.stderr, u'ERROR: can\'t open dump'
		exit(1)
	mydb = SqliteStorage()
	mydb.init()
	for q, s in enumerate(file):
		ok, result = splitsql(q, s)
		if ok:
			#print >> sys.stderr, q
			mydb.add(q, result)
		#if q > 1000000:
		mydb.commit()
		#	break
	file.close()
