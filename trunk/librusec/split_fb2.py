#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to split fb2 into header and images.
Input:
* stdin - fb2
* 1 - img prefix (dir/fileprefix)
Output:
* stdout - fb2 header
Errors:
* 1 - </description> not found
* 2 - bad description
* 3 - </binary> not found
* 4 - bad binary
Algo:
* cut off header (till </description>)
* add trailing </FicionBook>
* parse header to find all of <cover><image> and store href
* find all of <binary>..</binary>
* save if id is in hrefs
'''

import sys, os, base64
import xml.parsers.expat

reload(sys)
sys.setdefaultencoding('utf-8')

pfx = None
fb2 = None
parser_image = None
parser_binary = None
header = None
hrefs = set()
id = None
mime = None
binary = ''

def	start_image_element(name, attrs):
	global hrefs
	if name == 'image':
		for k, v in attrs.iteritems():
			if k.endswith('href') and v.startswith('#'):
				hrefs.add(v[1:])

def	start_binary_element(name, attrs):
	global id, mime, binary
	if attrs['id'] in hrefs:
		id = attrs['id']
		mime = attrs['content-type']

def	end_binary_element(name):
	global pfx, id, mime, binary
	if (id):
		with open(pfx + '_' + id, 'w') as f:
			f.write(base64.b64decode(binary))
		id = None
		mime = None
		binary = ''

def	char_data(cdata):
	global id, binary
	if (id):
		binary += cdata

def	prepare_parsers():
	global parser_binary
	parser_binary = xml.parsers.expat.ParserCreate()
	parser_binary.StartElementHandler = start_binary_element
	parser_binary.EndElementHandler = end_binary_element
	parser_binary.CharacterDataHandler = char_data

def	xtract_header():
	global fb2, header
	retvalue = fb2.find('</description>')
	if retvalue > 0:
		retvalue += 14
		header = fb2[:retvalue] + '</FictionBook>'
		try:
			parser_image.Parse(header, True)
		except:
			exit(2)
	return retvalue

def	xtract_images(start):
	global fb2
	idx0 = start
	retvalue = 0
	while (retvalue == 0):
		idx1 = fb2.find('<binary', idx0)
		if (idx1 > 0):
			idx2 = fb2.find('</binary>', idx1)
			if (idx2 > 0):
				idx2 += 9
				prepare_parsers()
				try:
					parser_binary.Parse(fb2[idx1:idx2], True)
				except:
					retvalue = 4
				idx0 = idx2
			else:
				retvalue = 3
		else:
			break
	return retvalue

def	main(fp):
	global pfx, fb2, header, parser_image
	parser_image = xml.parsers.expat.ParserCreate()
	parser_image.StartElementHandler = start_image_element
	fb2 = sys.stdin.read()
	eof = xtract_header()
	if eof < 0:
		exit(1)
	pfx = fp
	err = xtract_images(eof)
	if (err):
		exit(err)
	print header

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print >> sys.stderr, 'Usage: %s <imgprefix> < fb2' % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1])
