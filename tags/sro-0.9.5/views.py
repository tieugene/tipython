# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from settings import LOGIN_URL
from apps.sro2.jnj import jrender_to_response

def    index(request):
    return jrender_to_response('sro2/index.html', {'menus': (
        "gw/menu.html",
        "ref/menu.html",
        "sro2/menu.html",
    )},request)

def    about(request):
    return render_to_response('about.html', RequestContext(request))

def    common_context(context):
    '''
    our context processor. Add to dict vars to send in ALL templates.
    '''
    if context.path.startswith('/gw'):
        path='gw'
    else:
        path='sro2'
    return {
        'LOGIN_URL' : LOGIN_URL,
        'path':path
    }