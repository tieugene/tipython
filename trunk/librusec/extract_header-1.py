#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to cut off <body>es from fb2.
Input: stdin
Output: stdout
'''

import sys

output = True	#
idx0 = 0
data = sys.stdin.read()
while(True):
	if (output):
		idx1 = data.find('<body', idx0)
		if (idx1 > 0):
			sys.stdout.write(data[idx0:idx1])
			output = False
			idx1 = idx0
		else:
			sys.stdout.write(data[idx0:])
			break
	else:
		idx1 = data.find('</body>', idx0)
		if (idx1 > 0):
			output = True
			idx0 = idx1 + 7
		else:
			print "Can't close body"
			exit(1)
