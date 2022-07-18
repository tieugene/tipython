# -*- coding: utf-8 -*-
'''
'''
# 1. system
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 1. django
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

# 4. my
from wdp.dsfs import FSStorage
from wdp.dp import DavProvider
from wdp.lock import Locker


DS = FSStorage(settings.MEDIA_ROOT, Locker())
DP = DavProvider(DS)

@csrf_exempt
def	index(request, path):
	'''
	1. Fill header
	2. get user
	3. call with header, body and user
	'''
	#return HttpResponse()
	return DP.dispatch(request, path)
