#!/bin/env python
'''
Test of 5M objects in dict(dict) (50x100000)
Result: 200M
'''

import sys
from meminfo import getusedmem

print >> sys.stderr, "Start: ", getusedmem()
data = dict()
for i in xrange(50):
	model = "%08d" % i
	data[model]=dict()
	for j in xrange(100000):
		data[model][j]=j
print >> sys.stderr, "Start: ", getusedmem()
