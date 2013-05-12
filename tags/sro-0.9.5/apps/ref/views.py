# -*- coding: utf-8 -*-
'''
KLADR views
'''
# 1. django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
# 3. my
from models import *
from forms import *

def	index(request):
	return render_to_response('ref/index.html', context_instance=RequestContext(request))

def	__list_simple(request, html, model):
	return render_to_response(os.path.join('ref', html), context_instance=RequestContext(request, {'item_list': model.objects.all()}))

def	__list_hier(request, html, model):
	return render_to_response(os.path.join('ref', html), context_instance=RequestContext(request, {'item_list': model.get_root_nodes()}))

def	__view_hier(request, html, model, item_id):
	return render_to_response(os.path.join('ref', html), context_instance=RequestContext(request, {'item': model.objects.get(pk=item_id)}))

def	kladr_list(request):
	return __list_hier(request, 'kladr_list.html', Kladr)

def	kladr_view(request, item_id):
	return __view_hier(request, 'kladr_detail.html', Kladr, item_id)

def	okato_list(request):
	return __list_hier(request, 'okato_list.html', Okato)

def	okato_view(request, item_id):
	return __view_hier(request, 'okato_detail.html', Okato, item_id)

def	okopf_list(request):
	return __list_hier(request, 'okopf_list.html', Okopf)

def	okopf_view(request, item_id):
	return __view_hier(request, 'okopf_detail.html', Okopf, item_id)

def	oksm_list(request):
	return __list_simple(request, 'oksm_list.html', Oksm)
