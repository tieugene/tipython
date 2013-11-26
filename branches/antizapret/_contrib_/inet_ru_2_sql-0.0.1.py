#!/bin/env python
# -*- coding: utf-8 -*-
'''
Print all RU records (177236) as SQL records => can skip:
- fully commented records
- not inetnum records
Time: 3455862 lines / ~48klines/s = 1'11" @ P4-3.0
'''

import sys
from iptools.ipv4 import ip2long

def	main(fname):
	with open(fname, 'r') as f:
		net = None
		g_counter = 1
		l_counter = 1
		for l in f:
			#if (counter % 100000) == 0:
			#	print >> sys.stderr, counter/100000
			if (l == '\n'):
				pass
			elif (l.startswith('inetnum:')):	# generate net
				beg, end = l[16:].split(' - ')
				beg = ip2long(beg)
				end = ip2long(end)
				net = (beg << 32) | end
				print 'INSERT INTO ripe (id, beg, end) VALUES (%d, %d, %d);' % (net, beg, end)
				l_counter = 1
				continue
			else:
				print 'INSERT INTO ripec (id, net, c, k, v) VALUES (%d, %d, %d, \'%s\', \'%s\');' % (g_counter, net, l_counter, l[:16].rstrip().rstrip(':'), l[16:].strip())
				g_counter += 1
				l_counter += 1

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print 'Usage: %s <ripe.db.inetnum RU filename>'
	else:
		main(sys.argv[1])
