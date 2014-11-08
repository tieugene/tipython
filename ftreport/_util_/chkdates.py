#!/bin/env python
# -*- coding: utf-8 -*-
'''
Input:
- date (YYYY-MM-DD) == ft folder path
Time: 23"
'''

import flowtools
import os, sys, datetime

data	= dict()	# date: [mintime, maxtime, bytes]
dt_min	= sys.maxint
dt_max	= 0L

def	main(argv):
	global dt_min, dt_max
	root = argv[0]
	# 1. collect data
	for f in os.listdir(root):
		flowset = flowtools.FlowSet(os.path.join(root, f))
		for flow in flowset:
			dt = long(flow.last)
			if (dt < dt_min):
				dt_min = dt
			elif (dt > dt_max):
				dt_max = dt

			dt = datetime.datetime.fromtimestamp(long(flow.last))
	# 2. print
	dt_min = datetime.datetime.fromtimestamp(dt_min)
	dt_max = datetime.datetime.fromtimestamp(dt_max)
	tz = 0
	print dt_min, '..', dt_max, ", TZ =", tz

if (__name__ == '__main__'):
	if (len(sys.argv) != 2):
		print 'Usage: %s <folder>' % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1:])
