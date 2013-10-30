#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to cut off <body>es from fb2.
Input: stdin
Output: stdout
'''

import sys

output = True	#

for line in sys.stdin:
	if (output):
		if line == '<body>\n':
			output = False
		else:
			sys.stdout.write(line)
	else:
		if line == '</body>\n':
			output = True
