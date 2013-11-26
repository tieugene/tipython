#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to convert FB2 documents into HTML
'''

import sys, xml.sax
from xml.sax.handler import ContentHandler

class	FB2Handler(ContentHandler):
	def	__init__ (self):
		self.level = 0
		self.drop = False
		self.s = u''
		self.outtext = False
	def	startDocument(self):
		self.s += u'<html>\n'
	def	startElement(self, name, attrs):
		if name == 'a':
			s += u'<a href="">\n' % attrs.get('href',"")
		elif name == 'binary':
			pass
		elif name == 'p':
			if (not self.drop):
				s += u'<p>'
				self.outtext = True
		elif name in (			# just replace
			'annotation',
			'author',
			'body',
			'book-name',
			'book-title'
			):
			pass
		elif name in ('FictionBook',):	# skipdown
			pass
		else:
			print "Unknown element:", name
		return
	def	endElement(self, name):
		if name == 'p':
			if (not self.drop):
				s += u'</p>'
	def	characters (self, ch):
		if (self.outtext):
			self.s += ch
			self.outtext = False
	def	endDocument(self):
		self.s += u'</html>'
		print self.s

def	main(argv):
	#parser = make_parser()   
	#handler = FB2Handler()
	#parser.setContentHandler(handler)
	#parser.parse(open())
	xml.sax.parse(argv[0], FB2Handler())

if (__name__ == '__main__'):
	main(sys.argv[1:])
