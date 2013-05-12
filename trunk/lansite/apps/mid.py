# coding: utf-8
'''
Middleware
http://code.google.com/p/django-tools/
'''
__author__ = 'averrin'

#from django.utils.thread_support import currentThread
from threading import currentThread

_requests = {}

def get_request():
	return _requests[currentThread()]

class GlobalRequestMiddleware(object):
	def process_request(self, request):
		_requests[currentThread()] = request
