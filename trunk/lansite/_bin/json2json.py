#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
json2json - remaking input json into output.
10k lines:	10M
100k lines:	105M
500k lines:	526M
6M lines:	? 6GB
'''

import os, sys, json, pprint
from meminfo import getusedmem

reload(sys)
sys.setdefaultencoding("utf-8")

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <jsonfile>" % sys.argv[0]
		exit(0)
	print >> sys.stderr, "Start:", getusedmem()
	file = open(sys.argv[1], 'r')
	json.load(file)
	file.close()
	print >> sys.stderr, "End:", getusedmem()
