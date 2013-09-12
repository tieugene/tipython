#!/bin/env python
# -*- coding: utf-8 -*-
'''
Set parents into ripe table of antizapret.db
'''

import sys, sqlite3
from iptools.ipv4 import ip2long, long2ip

def	main(fname):
	counter = 0
	conn = sqlite3.connect(fname)
	c1 = conn.cursor()
	c2 = conn.cursor()
	for id, beg, end in c1.execute('SELECT id, beg, end FROM ripe ORDER BY id'):
		counter += 1
		size = end - beg
		c2.execute('SELECT id, end - beg AS size, beg, end FROM ripe WHERE beg <= ? AND end >= ? AND size > ? ORDER BY size DESC LIMIT 1', (beg, end, size))
		p = c2.fetchone()
		if (p):
			print '%s - %s: %s - %s' % (long2ip(beg), long2ip(end), long2ip(p[2]), long2ip(p[3]))
		else:
			print '%s - %s: None' % (long2ip(beg), long2ip(end))
		if counter > 20:
			break
	conn.close()

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print 'Usage: %s antizaqpret.db'
	else:
		main(sys.argv[1])
