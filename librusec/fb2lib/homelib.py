#!/bin/env python
# -*- coding: utf-8 -*-
'''
as is - 48.67, 43.6
dummy start_elements - 39.8
try-except - 42.6
dummy parser - 23
so: till parser - 52%
parse - 40%
start.el - 8%
'''

import sys, os, zipfile, hashlib, pprint
import xml.parsers.expat, magic

mime = magic.open(magic.MIME_TYPE)
mime.load()
tags = dict()
files = 0

reload(sys)
sys.setdefaultencoding('utf-8')

def start_element(name, attrs):
	#tags[name] = tags[name] + 1 if name in tags else 1
    try:
        tags[name] += 1
    except:
        tags[name] = 1

def	parse_dir(fn):
	dirlist = os.listdir(fn)
	dirlist.sort()
	for i in dirlist:
		parse_file(os.path.join(fn, i))

def	parse_file(fn):
	m = mime.file(fn)
	if (m == 'application/zip'):
		parse_zip(fn)
	elif (m == 'application/xml'):
		parse_fb2(fn)
	else:
		print >> sys.stderr, 'Unknown mime type (%s) of file %s' % (m, fn)

def	parse_zip(fn):
	print >> sys.stderr, 'Zip:', os.path.basename(fn)
	z = zipfile.ZipFile(fn, 'r')
	filelist = z.namelist()
	filelist.sort()
	for n in filelist:
		try:
			parse_fb2(z.open(n))
			print >> sys.stderr, n
		except:
			print >> sys.stderr, 'X:', n

def	parse_fb2(fn):
	global files
	if isinstance(fn, str):
		fn = open(fn)
	parser = xml.parsers.expat.ParserCreate()
	parser.StartElementHandler = start_element
	#a = fn.read()
	parser.Parse(fn.read(), True)
	files += 1

def	print_result():
	#out = open('result.txt', 'w')
	for k, v in tags.iteritems():
		print u'%s\t%d' % (k, v)
		#out.write(u'%s\t%d\n' % (k, v))
	#print 'Files:', files

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print >> sys.stderr, 'Usage: %s <xmlfile|zipfile|folder>' % sys.argv[0]
		sys.exit(1)
	src = sys.argv[1]
	if (os.path.isdir(src)):
		parse_dir(src)
	else:
		parse_file(src)
	print_result()
