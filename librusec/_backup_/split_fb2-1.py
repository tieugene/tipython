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

Result: 193 files on 1'14.5" (2.6 fps)
'''

import sys, os, base64, zipfile
import xml.parsers.expat

reload(sys)
sys.setdefaultencoding('utf-8')

ipfx = None
fb2 = None
parser_image = None
parser_binary = None
header = None
hrefs = set()
id = None
mime = None
binary = ''

errcode = {
	1: '</description> not found',
	2: 'invalid description',
	3: '</binary not found',
	4: 'invalid binary',
}

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
	global ipfx, id, mime, binary
	if (id):
		with open(ipfx + '_' + id, 'w') as f:
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
			retvalue = -2
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

def	parse_fb2(z, fn, hdir, idir):
	'''

	@param fp - prefix
	'''
	global ipfx, fb2, header, parser_image, hrefs
	# prepare filenames and folders
	n, e = fn.split('.')
	fullname = '%06d' % int(n)
	dirname = fullname[:3]
	# let's go
	parser_image = xml.parsers.expat.ParserCreate()
	parser_image.StartElementHandler = start_image_element
	fb2 = z.open(fn).read()
	hrefs.clear()
	eof = xtract_header()
	if eof < 0:
		return 0-eof
	idir = os.path.join(idir, dirname)
	if not os.path.exists(idir):
		os.mkdir(idir)
	ipfx = os.path.join(idir, fullname)
	err = xtract_images(eof)
	if (err):
		return err
	hdir = os.path.join(hdir, dirname)
	if not os.path.exists(hdir):
		os.mkdir(hdir)
	with open(os.path.join(hdir, fullname+'.xml'), 'w') as f:
		f.write(header)

def	parse_zip(zn, hdir, idir):
	z = zipfile.ZipFile(zn, 'r')
	filelist = z.namelist()
	filelist.sort()
	for fn in filelist:
		#print fn
		err = parse_fb2(z, fn, hdir, idir)
		if err:
			print >> sys.stderr, fn, errcode[err]

if (__name__ == '__main__'):
	if len(sys.argv) != 4:
		print >> sys.stderr, 'Usage: %s <zipfile> <hdrdir> <imgdir>' % sys.argv[0]
		sys.exit(1)
	parse_zip(sys.argv[1], sys.argv[2], sys.argv[3])
