#!/bin/env python
# -*- coding: utf-8 -*-
'''
'''

import os, sys, pprint
from PIL import Image, ImageSequence

if (__name__ == '__main__'):
	if len(sys.argv) != 2:
		print "Usage: %s <file>" % sys.argv[0]
		exit(0)
	im = Image.open(sys.argv[1], 'r')
	if not im:
		print >> sys.stderr, "Can't open image"
		exit(0)
	size = im.size
	print "Size: %d x %d, Format: %s, Mode: %s" % (size[0], size[1], im.format, im.mode)
	pprint.pprint(im.info)
	index = 0
	for frame in ImageSequence.Iterator(im):
	    index = index + 1
	print index
