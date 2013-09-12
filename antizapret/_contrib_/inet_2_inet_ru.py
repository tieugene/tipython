#!/bin/env python
# -*- coding: utf-8 -*-
'''
Print all RU records from ripe.db.inetnum (87460870 lines; ~300K lines/s @ P4-3.0)
'''

import sys

def	main(fname):
	with open(fname, 'r') as f:
		newrec = True
		inetnumrec = False
		rurec = False
		toflush = False
		buffer = list()
		counter = 0
		for l in f:
			counter += 1
			if (counter % 1000000) == 0:
				print >> sys.stderr, counter/1000000
			if l.startswith('#'):		# skip fully commented lines
				continue
			if (l == '\n'):			# not empty line => start new record
				if buffer:
					if rurec:	# flush previous buffer
						print ''.join(buffer)
					buffer[:] = []
				newrec = True
				continue
			if (newrec):
				newrec = False
				inetnumrec = l.startswith('inetnum:')
				rurec = False
			if (not inetnumrec):
				continue
			buffer.append(l)
			if l.startswith('country:') and l[16:18].upper() == 'RU':
				rurec = True
		if buffer and rurec:			# flush last buffer
			print '\n'.join(buffer)

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print 'Usage: %s <ripe.db.inetnum filename>'
	else:
		main(sys.argv[1])
