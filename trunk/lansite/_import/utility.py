#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
meminfo.py - get used system memory
'''

import subprocess
from datetime import datetime

def	__getmem(s):
	i =  subprocess.Popen(['grep', '^' + s], stdin=subprocess.Popen(['cat', '/proc/meminfo'], stdout=subprocess.PIPE).stdout, stdout=subprocess.PIPE).communicate()[0].split(':')[1].strip().strip('kB')
	return long(i)

def	getusedmem():
	'''
	MemTotal - MemFree - Buffers - Cached
	'''
	return __getmem('MemTotal') - __getmem('MemFree') - __getmem('Buffers') - __getmem('Cached')

def	now():
	return datetime.now().strftime("%H:%M:%S")
