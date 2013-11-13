#!/bin/env python
'''
Спотыкается на 'И'
не понимает 1251
'''

import sys, os, pprint
import xml.sax.handler

data = dict()

class Handler(xml.sax.handler.ContentHandler):
    def startElement(self, name, attrs):
        data[name] = data[name] + 1 if name in data else 1

def	main(fn):
	xml.sax.parse(open(fn), Handler())

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <xmlfile>" % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
	pprint.pprint(data)
