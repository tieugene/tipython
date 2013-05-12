# -*- coding: utf-8 -*-
'''
Shared views
----------

Averrin comments syntax:

    Title of function
    # Comments (including TODO and !!!WARNINGS!!!)

    @type name -- purpose of input params

    * how
    * function
    * do this

    <type:name -- purpose of output params (to template inside HttpResponse)
'''
# 1. django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse 
from django.db import transaction
from django.db.models import Q, Count, Avg, Max, Min
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
from django.views.generic.simple import direct_to_template
import sys, ftplib, netrc, tempfile, csv, pprint, itertools
from datetime import datetime, date as dt
from trml2pdf import trml2pdf
import time
# 2. own
from models import *
###(1
from gw.models import *
###1)
from forms import *
from settings import STATIC_ROOT, MEDIA_ROOT, VERSION
# 3. RTF
from rtfng.utils import RTFTestCase
from rtfng.Elements import Document
from rtfng.document.section import Section
from rtfng.document.paragraph import Cell, Paragraph, Table
from rtfng.PropertySets import BorderPropertySet, FramePropertySet, ParagraphPropertySet, TabPropertySet
from rtfng.document.character import TEXT, Text
from rtfng.PropertySets import TextPropertySet
from rtfng.document.base import TAB, LINE
from sro2.history.views import History
from django.core.exceptions import PermissionDenied

reload(sys)
sys.setdefaultencoding("utf-8")

from sro2.jnj import *

def drender_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

#@login_required
def	log_it(request, object, action, change_message=''):
    '''
    Log this activity
    '''
    LogEntry.objects.log_action(
        user_id		 = request.user.id,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id	   = object.pk,
        object_repr	 = object.asstr(), # Message you want to show in admin action list
        change_message  = u'SRO2.UI: ' + change_message, # I used same
        action_flag	 = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
    )


@render_to('sro2/error.html')
def err500(request):
    return {}

def err(request):
    raise Exception('boom')

def log(request):
    sro=SroOwn.objects.get(pk=1)
    result=sro.save
    return HttpResponse(str(sro.__dict__))

def	pdf_render_to_response(template, context, filename=None):
    '''
    Create pdf from rml-template and return file to user
    '''
    response = HttpResponse(mimetype='application/pdf')
    if not filename:
        filename = template+'.pdf'
    response['Content-Disposition'] = '; filename=%s' % filename
    tpl = loader.get_template(template)
    tc = {'filename': filename, 'STATIC_ROOT' : STATIC_ROOT}
    tc.update(context)
    response.write(trml2pdf.parseString(tpl.render(Context(tc)).encode('utf-8')))
    #response.write(tpl.render(Context(tc)).encode('utf-8'))
    return response


def	strdate(d):
    __mon = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря')
    return u'«%02d» %s %d года' % (d.day, __mon[d.month - 1], d.year)


def	strdatedot(date):
    if date:
        date = str(date).split('-')
        date ='%s.%s.%s' % (date[2], date[1], date[0])
        return date
    else:
        return ''

@login_required
@render_to('sro2/index.html')
def	index(request):
    '''
    Serve main page
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('../login/?next=%s' % request.path)
    jyears = LogEntry.objects.dates('action_time', 'year')
    return {}




def	get_uniq_permits(orgsro):
    history=History(orgsro)
    return history.originals()


def	upload_dict(orgsro):
    #history = get_history(orgsro)
    if (orgsro.currperm):
        history = orgsro.stagelist_set.instance_of(Permit).order_by('-permit__date').filter(permit__no=orgsro.currperm.no).exclude(id=orgsro.currperm.id)
        #history = orgsro.stagelist_set.instance_of(Permit).order_by('-permit__date').filter(permit__no=orgsro.currperm.no).exclude(id=orgsro.currperm.id)
    else:
        history = None
    permits = get_uniq_permits(orgsro)
    personsro_list = orgsro.sro.personorgsro_set.filter(org=orgsro.org).values_list('person')
    return {
        'orgsro': orgsro,
        'person_list': orgsro.org.orgstuff_set.filter(person__in=personsro_list, enddate__isnull=True, leader=True).order_by('person'),
        'permits': permits,
        'history': history
    }

@login_required
def	get_danger(request):
    if 'danger' in request.GET:
        if request.GET['danger'] == '1':
            danger = 1
        else:
            danger = 0
    else:
        danger = 0
    return danger

def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner
