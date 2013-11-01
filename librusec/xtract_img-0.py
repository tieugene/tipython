#!/bin/env python
# -*- coding: utf-8 -*-
'''
'''

import sys, os, base64
import xml.parsers.expat

reload(sys)
sys.setdefaultencoding('utf-8')

id = None
mime = None
data = None

def start_element(name, attrs):
    global id, mime
    id = attrs['id']
    mime = attrs['content-type']

def char_data(cdata):
    global data
    data = base64.b64decode(cdata)

def	main(fp):
	global data
	parser = xml.parsers.expat.ParserCreate()
	parser.StartElementHandler = start_element
	parser.CharacterDataHandler = char_data
	parser.Parse(sys.stdin.read(), True)
	with open(fp + '_' + id, "w") as f:
		f.write(data)
	#print id, mime

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print >> sys.stderr, 'Usage: %s <outputprefix> < binarychunk' % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
