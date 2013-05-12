#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Stage #2: PostSqlite - script to prepare sqlite db to import.
* rename parent fields (by ctid)
* delete orphan parents?
Inheritance:
Object
	#ObjectSq(Object)
	Address(Object)
	Email(Object)
	IM(Object)
	__URL(Object)
	WWW(Object)
	Phone(Object)
	TaggedObjectTag(Object)
	File(Object)
		ImageFile(File)
	Contact(Object)
		Org(Contact)
		Person(Contact)
	Task(Object)
		vCal(Task)
			vEvent(vCal)
			vToDo(vCal)
'''

import os, sys, gzip, re, sqlite3, datetime, pprint
#from meminfo import getusedmem

reload(sys)
sys.setdefaultencoding("utf-8")

def	now():
	return datetime.datetime.now().strftime("%H:%M:%S")

class	SqliteStorage:
	def	__init__(self):
		self.con = None
		self.cur = None
	def	init(self):
		self.con = sqlite3.connect('data.db')
		self.cur = self.con.cursor()
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
				self.cur.execute("INSERT INTO data (model, record, field, value) VALUES ('%s', %d, '%s', %s);" % (r[0], r_id, n, v))
			except:
				print >> sys.stderr, "INSERT INTO data (model, record, field, value) VALUES ('%s', %d, '%s', %s);" % (r[0], r_id, n, v)
		return True

	def	commit(self):
		self.con.commit()

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <dbname>" % sys.argv[0]
		exit(0)
	mydb = SqliteStorage()
	mydb.init()
	print >> sys.stderr, now(), "Start"
	print >> sys.stderr, now(), "To flush"
	mydb.commit()
	print >> sys.stderr, now(), "The End"
