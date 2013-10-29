#!/bin/env python
'''
'''

import sys, os
from lxml import etree

data = dict()

class Handler(object):
    def start(self, name, attrib):
        data[name] = data[name] + 1 if name in data else 1
    def end(self, tag):
        pass
    def data(self, data):
	pass
    def close(self):
        pass

parser = etree.XMLParser(target = Handler())

def	main(fn):
	results = etree.parse(fn, parser)

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <xmlfile>" % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
	pprint.pprint(data)
