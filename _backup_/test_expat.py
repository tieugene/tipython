#!/bin/env python
'''
"Supports utf8, utf16, latin1, ascii" - ok
'''

import sys, os, pprint
import xml.parsers.expat

data = dict()

def start_element(name, attrs):
	data[name] = data[name] + 1 if name in data else 1

parser = xml.parsers.expat.ParserCreate()
parser.StartElementHandler = start_element

def	main(fn):
	parser.Parse(open(fn).read())

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <xmlfile>" % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
	pprint.pprint(data)
