#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to stat fb2s.
Input:
* 1 - src dir
Output:
* stdout - fb2 header
Result: 6'45" (1240 fps)
TODO:
	* add fn column for dicts
'''

import sys, os
from xml.dom import minidom
import xml.parsers.expat

reload(sys)
sys.setdefaultencoding('utf-8')

OUTDIR = 'stat'

# mandatory
genres = dict()
langs = dict()
annot_tags = dict()
authors = dict()
# optional
#dates = set()

#parser = None
state = 0	# 0 = not started (wait for title-info), 1 - title-info, 2 - skip
substate = 0	# 0 - right in title-info, 1 - in author, 2 - in annotation
cur_tag = None
cur_author = dict()	# last, 1st, mid, nick, id, count

def	update_set(s, v):
	if v not in s:
		s.add(v)

def	update_dict(d, k):
	if k in d:
		d[k] += 1
	else:
		d[k] = 1

def	start_tag(name, attrs):
	global state, substate, annot_tags, cur_tag, cur_author
	if (state == 2):	# after title-info
		return
	if (state == 0):	# before title-info
		if (name == 'title-info'):
			state = 1
			substate = 0
		return
	# inside title-info
	if (substate == 0):	# title-info
		if (name == 'author'):
			substate = 1
			cur_author.clear()
		elif (name == 'annotation'):
			substate = 2
		cur_tag = name
	elif (substate == 1):	# author
		cur_tag = name
	else:			# annotation
		update_dict(annot_tags, name)

def	end_tag(name):
	global state, substate, authors, cur_tag, cur_author
	if (state != 1):	# out from title-info
		return
	if (name == 'title-info'):
		state = 2
		return
	# inside title-info
	cur_tag = None
	if (substate):
		if (substate == 1):
			if (name == 'author'):
				author = (
					cur_author.get('last-name', ''),
					cur_author.get('first-name', ''),
					cur_author.get('middle-name', ''),
					cur_author.get('nickname', ''),
					cur_author.get('id', ''),
				)
				# flush author
				if author in authors:
					authors[author] += 1
				else:
					authors[author] = 1
				substate = 0
		else:
			if (name == 'annotation'):
				substate = 0

def	char_data(cdata):
	global state, substate, cur_tag, cur_author
	if (state != 1):	# out from title-info
		return
	# inside title-info
	if (substate != 2):
		if (substate == 0):
			if (cur_tag == 'genre'):
				update_dict(genres, cdata)
			if (cur_tag == 'lang'):
				update_dict(langs, cdata)
		elif (substate == 1):
				cur_author[cur_tag] = cdata.strip()

def	mk_parser():
	#global parser
	parser = xml.parsers.expat.ParserCreate()
	parser.StartElementHandler = start_tag
	parser.EndElementHandler = end_tag
	parser.CharacterDataHandler = char_data
	return parser

def	process_fb2(hpath):
	#minidom.parse(hpath)
	#print hpath
	global state
	with open(hpath, 'r') as f:
		parser = mk_parser()
		state = 0
		parser.ParseFile(f)

def	results(odir):
	def	out_one(fn, d):
		with open(fn, 'w') as f:
			l = d.keys()
			l.sort()
			for k in l:
				f.write('%s\t%s\n' % (k, d[k]))
	out_one(os.path.join(odir, 'genres.lst'), genres)
	out_one(os.path.join(odir, 'langs.lst'), langs)
	out_one(os.path.join(odir, 'annotags.lst'), annot_tags)
	with open(os.path.join(odir, 'authors.lst'), 'w') as f:
		l = list()
		for k, v in authors.iteritems():
			l.append('%s\t%s' % ('\t'.join(k), v))
		l.sort()
		f.write('\n'.join(l))

def	main(hdir, odir):
	counter = 0
	pfxlist = os.listdir(hdir)
	pfxlist.sort()
	for pfx in pfxlist:
		pdir = os.path.join(hdir, pfx)
		hdrlist = os.listdir(pdir)
		hdrlist.sort()
		for hdr in hdrlist:
			#print hdr
			process_fb2(os.path.join(pdir, hdr))
			#counter += 1
			#if (counter == 100):
			#	break
		#break
	results(odir)

if (__name__ == '__main__'):
	if len(sys.argv) != 3:
		print >> sys.stderr, 'Usage: %s <hdrdir> <outdir>' % sys.argv[0]
		sys.exit(1)
	main(sys.argv[1], sys.argv[2])
