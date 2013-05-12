# -*- coding: utf-8 -*-
'''
Stagelist views
--------------
'''
from sro2.shared import *

@login_required
def    stagelist_view(request, stagelist_id, full, danger):
    
    stagelist = StageList.objects.get(pk=stagelist_id)
    
    if stagelist.isperm():
        return redirect('sro2.views.permit_view',permit_id=stagelist_id,full=full,danger=danger)    
        
    if stagelist.isstatement():
        return redirect('sro2.views.statement_view',statement_id=stagelist_id,full=full,danger=danger)        

@login_required
def    stagelist_edit(request, stagelist_id):
    
    stagelist = StageList.objects.get(pk=stagelist_id)
    
    if stagelist.isperm():
        return redirect('sro2.views.permit_edit',permit_id=stagelist_id)    
        
    if stagelist.isstatement():
        return redirect('sro2.views.statement_edit',statement_id=stagelist_id)
        
@login_required
@render_to('sro2/stagelist/stagelist_html.html')
def    stagelist_html(request, stagelist_id):
    return {'stagelist': StageList.objects.get(pk=stagelist_id)}

@login_required
@render_to('sro2/stagelist/stagelist_compare.html')
def    stagelist_compare(request, stagelist_id):
    '''
    Page with compare form
    '''
    stagelist = StageList.objects.get(pk=stagelist_id)
    return {
        'stagelist': stagelist,
        'compareto': CompareToForm(stagelist),
    }

@login_required
@transaction.commit_manually
def    stagelist_editstages(request, stagelist_id):
    '''
    Editing stages in stagelist

    * get checked items from form
    * get stages from db
    * compare:
        * del deleted
        * add new (w/ date=None)
        * don't touch common

    '''
    danger = get_danger(request)
    stagelist = StageList.objects.get(pk=stagelist_id)
    if request.method == 'POST':    # no valid - just save
        # 1. delete all
        result = False
        ps = stagelist.permitstage_set
        ids_old = set(ps.filter(danger=danger).values_list('stage', flat=True))
        ids_new = set(map(int, request.POST.getlist('id')))
        ids_del = ids_old - ids_new
        ids_add = ids_new - ids_old
        try:
        #if (True):
            if ids_del:
                ps.filter(danger=danger, stage__in=ids_del).delete()
            for i in ids_add:
                PermitStage(stagelist=stagelist, stage=Stage.objects.get(pk=i), danger=danger).save()
        except:
            transaction.rollback()
        else:
            transaction.commit()
            result = True
        if (result):
            if (ids_del or ids_add):
                #log_it(request, stagelist, CHANGE, u'Виды работ')
                transaction.commit()
        return HttpResponseRedirect(reverse('sro2.views.stagelist_view', kwargs={
            'stagelist_id': stagelist.id,
            'full': 0,
            'danger': int(danger),
        }))
        
    else:    # GET
        return jrender_to_response('sro2/stagelist/stagelist_edit_stage.html', {
            'stagelist': stagelist,
            'itemlist': stagelist.permitstage_set.dict_extra(stagelist, danger),
            'danger': int(danger)
        },request)
        
@login_required
def    stagelist_dup(request, stagelist_id):
    
    if request.method == 'POST':
        if request.POST['type_id']:
            if request.POST['type_id'] == 'statement':
                return HttpResponseRedirect(reverse('sro2.views.statement_dup', kwargs={ 'statement_id': stagelist_id }))
            else:
                return HttpResponseRedirect(reverse('sro2.views.permit_dup', kwargs={ 'permit_id': stagelist_id }))
    
    return HttpResponseRedirect(reverse('sro2.views.stagelist_view', kwargs={
        'stagelist_id': stagelist_id,
        'full': 0,
        'danger': 0,
    }))    
    
@login_required
@render_to('sro2/stagelist/stagelist_cmp.html')
def    stagelist_cmp(request, permit_id):
    '''
    Compare 2 stagelists:

    * deleted
    * added
    * changed
    '''
    
    stagelist_s = StageList.objects.get(pk=permit_id)
    hist=History(stagelist_s.orgsro)
    form = CompareToForm(stagelist_s, request.POST)
    if form.is_valid():
        stagelist_d = form.cleaned_data['other']
        deleted, added, common = hist.cmp_stagelists(stagelist_s, stagelist_d)
        return {
            'src':        stagelist_s,
            'dst':        stagelist_d,
            'del_o':    deleted.filter(danger=False),
            'del_d':    deleted.filter(danger=True),
            'add_o':    added.filter(danger=False),
            'add_d':    added.filter(danger=True),
            'chg_o':    common.filter(danger=False),
            'chg_d':    common.filter(danger=True),
        }

@login_required
@render_to('sro2/stagelist/stagelist_cmp.html')
def    stagelist_cmp_ajax(request, stagelist_id, dest_id):
    '''
    для приостановки/возобновления работ по отдельности
    
    Get comparing information and return to ajax

    # difference from next function -- ids get from url, not from submitted form
    '''
    stagelist_s = StageList.objects.get(pk=stagelist_id)
    stagelist_d = StageList.objects.get(pk=dest_id)
    hist=History(stagelist_s.orgsro)
    deleted, added, common = hist.cmp_stagelists(stagelist_s, stagelist_d)
    return {
        'src':        stagelist_s,
        'dst':        stagelist_d,
        'del_o':    deleted.filter(danger=False),
        'del_d':    deleted.filter(danger=True),
        'add_o':    added.filter(danger=False),
        'add_d':    added.filter(danger=True),
        'chg_o':    common.filter(danger=False),
        'chg_d':    common.filter(danger=True),
    }

