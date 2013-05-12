# coding: utf-8
__author__ = 'averrin'
""" Middleware """

from django.utils.thread_support import currentThread
_requests = {}

def get_request():
    req=_requests
    res=req[currentThread()]
    return res

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        _requests[currentThread()] = request
