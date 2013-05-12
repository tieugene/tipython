
# -*- coding: utf-8 -*-
'''
Sro views
-------------
'''
from sro2.shared import *

@render_to('sro2/sro/sro_list.html')
def sro_list(request):
    sros=SroOwn.objects.all()
    return {'sros':sros}

@render_to('sro2/sro/sro_new.html')
def sro_new(request):
    if not request.method == 'POST':
        soform=SroOwnForm()
        sform=SroForm()
        return {'soform':soform,'sform':sform}
    else:
        return sro_save(request)

@render_to('sro2/sro/sro_edit.html')
def sro_edit(request,sro_id):
    if not request.method == 'POST':
        sro=SroOwn.objects.get(pk=sro_id)
        soform=SroOwnForm(instance=sro)
        sform=SroForm(instance=sro.sro)
        return {'sro':sro,'soform':soform,'sform':sform}
    else:
        return sro_save(request,sro_id)

def sro_save(request,sro_id=''):
    if not sro_id:
        soform=SroOwnForm(request.POST)
        sform=SroForm(request.POST)
    else:
        so=SroOwn.objects.get(pk=sro_id)
        soform=SroOwnForm(request.POST,instance=so)
        sform=SroForm(request.POST,instance=so.sro)
    if sform.is_valid() and soform.is_valid():
        if not sro_id:
            item=sform.save()
            so=soform.save(commit=False)
            so.sro=item
            so.save()
        else:
            soform.save()
            sform.save()
        return redirect(sro_view,sro_id=so.id)
    else:
        if not sro_id:
            return jrender_to_response('sro2/sro/sro_new.html', {'sform':sform,'soform':soform},request)
        else:
            return jrender_to_response('sro2/sro/sro_edit.html', {'sform':sform,'soform':soform,'sro':Sro.objects.get(pk=sro_id)},request)

def sro_del(request,sro_id):
    so=SroOwn.objects.get(pk=sro_id)
    so.sro.delete()
    so.delete()
    return redirect(sro_list)

@render_to('sro2/sro/sro_view.html')
def sro_view(request,sro_id):
    sro=SroOwn.objects.get(pk=sro_id)
    return {'sro':sro}