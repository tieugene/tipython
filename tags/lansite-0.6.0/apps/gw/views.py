# -*- coding: utf-8 -*-
'''
lansite.gw.views.py
'''

# 0. trash
##from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
##from django.contrib.contenttypes.models import ContentType
#from django.core.urlresolvers import reverse, resolve
#from django.db import transaction
##from django.db.models import Q
##from django.forms.util import ErrorList
#from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader, Context, RequestContext
##from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
#from django.contrib.auth.decorators import login_required, permission_required
#from django.shortcuts import get_object_or_404, render_to_response

# 1. django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from bits.views import *
from contact.views import *
from task.views import *

@login_required
def	index(request):
	return render_to_response('gw/index.html')
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
	return render_to_response('gw/index.html')
