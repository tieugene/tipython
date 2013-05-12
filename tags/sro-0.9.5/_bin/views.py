# -*- coding: utf-8 -*-
'''
Permit views
------------
'''
from sro2.shared import *

@login_required
def    permit_add(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = PermitAddForm(request.POST)
        if form.is_valid():
            permit = None
            try:
                permit = Permit(
                    no=form.cleaned_data['no'],
                    date=form.cleaned_data['date'],
                    protocol=form.cleaned_data['protocol'],
                    statement=form.cleaned_data['statement'],
                    orgsro=orgsro,
                    ver=form.cleaned_data['ver']
                )
                permit.save()
            except:
                transaction.rollback()
            else:
                transaction.commit()
            if permit is not None:
                log_it(request, permit, ADDITION)
                transaction.commit()
            return redirect('sro2.views.orgsro_stagelist_edit',orgsro_id=orgsro.id)
    else:
        form = PermitAddForm()
    form.setdata(orgsro)
    return render_to_response('sro2/stagelist/stagelist_add.html', RequestContext(request, {'orgsro': orgsro, 'form': form, 'type': 'Свидетельство'}))

@login_required
def    permit_del(request, permit_id):

    permit = StageList.objects.get(pk=permit_id)
    orgsro_id = permit.orgsro.id
    orgsro = OrgSro.objects.get(pk=orgsro_id)

    try:
        if permit == orgsro.currperm:
            # clearing the value of the field "currperm" for model "OrgSro" before deleting current permit
            log_it(request, orgsro, CHANGE)
            orgsro.currperm = None
            orgsro.save()        

        # deleting of snapshots
        snap_list = orgsro.stagelist_set.instance_of(Permit).filter(permit__no=permit.no)
        log_it(request, permit, DELETION)
        for snap in snap_list:
            snap.delete()
    except:
        pass

    return redirect('sro2.views.orgsro_stagelist_edit',orgsro_id=orgsro.id)

@login_required
def    permit_view(request, permit_id, full, danger):

    stagelist = StageList.objects.get(pk=permit_id)
    full = int(full)
    danger = int(danger)

    prevperms = stagelist.orgsro.stagelist_set.instance_of(Permit).filter(permit__no=stagelist.no).order_by('permit__date')
    prevperm = prevperms[len(prevperms)-1]
    if prevperms.count() == 1: # one permit exists always 
        issnapshots = False
    else:
        issnapshots = True

    form=ProtocolListForm()
    form.setdataD(stagelist.orgsro)    
    hist=History(stagelist.orgsro)

    stagelist.permit.last=hist.last_snap(stagelist.permit)

    if not full:
        return render_to_response('sro2/stagelist/stagelist_view.html', RequestContext(request, {
            'prevpermit_id': prevperm.id,
            'prevdate': strdatedot(prevperm.date),
            'stagelist': stagelist,
            'itemlist': prevperm.permitstage_set.dict(danger),
            'canedit': checkuser(stagelist.orgsro.org, request.user),
            'canedit_orgsro': checkuser(stagelist.orgsro, request.user),
            'danger': int(danger),
            'button': prevperm.status,
            'issnapshots': issnapshots,
            'form': form,
            'full': 0,
            }))
    else:
        return render_to_response('sro2/stagelist/stagelist_full.html', RequestContext(request, {
            'prevpermit_id': prevperm.id,
            'prevdate': strdatedot(prevperm.date),                
            'stagelist': stagelist,
            'itemlist': stagelist.permitstage_set.dict_extra(stagelist, danger),
            'canedit': checkuser(stagelist.orgsro.org, request.user),
            'canedit_orgsro': checkuser(stagelist.orgsro, request.user),
            'danger': int(danger),
            'button': prevperm.status,
            'issnapshots': issnapshots,
            'form': form,
            'full': 1,
            }))

@login_required
def    permit_resetdefault(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    orgsro.currperm = None
    orgsro.save()

    return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={
        'orgsro_id': orgsro.id,
    }) + "#permit")

@login_required
def    permit_setdefault(request, permit_id):
    permit = StageList.objects.get(pk=permit_id)
    orgsro = permit.orgsro
    orgsro.currperm = permit
    orgsro.save()
    return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={
        'orgsro_id': orgsro.id
    }) + "#permit")


@login_required
def    permit_pdf(request, permit_id):
    stagelist = StageList.objects.get(pk=permit_id)
    from datetime import datetime, date, time, timedelta
    if stagelist.ver.id == 2: # new order 624
        # this orgsro, permit, date < this, order by date desc - 1st
        prevperms = StageList.objects.filter(orgsro = stagelist.orgsro, permit__date__lt = stagelist.permit.date).order_by('-permit__date')
        if prevperms:
            prevperm = prevperms[0]
        else:
            prevperm = None
        stages_o = stagelist.stages.filter(permitstage__danger = False)
        stages_d = stagelist.stages.filter(permitstage__danger = True)    # All danger
        o = set(stages_o.values_list('id', flat=True))
        d = set(stages_d.values_list('id', flat=True))
        stages = Stage.objects.filter(ver = stagelist.ver, srotype = stagelist.orgsro.sro.type).distinct().order_by('id')

        cf = int(stagelist.orgsro.paysum)

        if stagelist.orgsro.sro.id == 2: # МООАСП
            cf_text1 = 'С правом осуществлять организацию работ по подготовке проектной документации, стоимость которой по одному договору'
            if cf >= 150000: #and ins>=10000000:
                cf_text2 = ' не превышает пять миллионов рублей.'
            if cf >= 250000: #and ins>=20000000:
                cf_text2 = ' не превышает двадцать пять миллионов рублей.'
            if cf >= 500000: #and ins>=30000000:
                cf_text2 = ' не превышает пятьдесят миллионов рублей.'
            if cf >= 1000000: #and ins>=100000000:
                cf_text2 = ' составляет до трехсот миллионов рублей.'
            if cf >= 1500000: #and ins>=200000000:
                cf_text2 = ' составляет триста миллионов рублей и более.'

        if stagelist.orgsro.sro.id == 1: # МООЖС
            cf_text1 = 'С правом осуществлять организацию работ по строительству, стоимость которого по одному договору'
            if cf >= 300000: #and ins>=10000000:
                cf_text2 = ' не превышает десять миллионов рублей.'
            if cf >= 500000: #and ins>=20000000:
                cf_text2 = ' не превышает шестьдесят миллионов рублей.'
            if cf >= 1000000: #and ins>=30000000:
                cf_text2 = ' не превышает пятьсот миллионов рублей.'
            if cf >= 2000000: #and ins>=100000000:
                cf_text2 = ' не превышает три миллиарда рублей.'
            if cf >= 3000000: #and ins>=200000000:
                cf_text2 = ' не превышает десять миллиардов рублей.'                                                                                                                                                                                                                                                                                          if cf >= 10000000: #and ins>=200000000:
            if cf >= 10000000: #and ins>=200000000:
                cf_text2 = ' составляет десять миллиардов рублей и более.'

        data = {
            'stagelist': stagelist,
            'stages': stages,
            'o': o,
            'd': d,
            'prevperm': prevperm,
            'date': strdate(stagelist.permit.date),
            'protodate': strdate(stagelist.permit.protocol.date),
            'user': request.user.username,
            'cf_text1': cf_text1,
            'cf_text2': cf_text2,
        }
        borderdate=date(2010,8,9)
        '''if stagelist.permit.date<borderdate:
            template_name = os.path.join('sro2', 'perm_%s_prev.rml' % data['stagelist'].orgsro.sro.sroown.tplprefix)
        else:
            template_name = os.path.join('sro2', 'perm_%s.rml' % data['stagelist'].orgsro.sro.sroown.tplprefix)'''
        template_name = os.path.join('sro2', 'perm_%s.rml' % data['stagelist'].orgsro.sro.sroown.tplprefix)

    else: # old order 574
        data = {
            'stagelist': stagelist,
            'date': strdate(stagelist.permit.date),
            'protodate': strdate(stagelist.permit.protocol.date),
            'user': request.user.username,
        }
        template_name = os.path.join('sro2', 'perm_%s_old.rml' % data['stagelist'].orgsro.sro.sroown.tplprefix)

    return pdf_render_to_response(template_name, {'data': data}, filename=data['stagelist'].permit.no + '.pdf')

@login_required
#@transaction.commit_manually
def    permit_pause_allstages(request, permit_id):
    '''
    Pauseing all stages in permit

    # TODO: return commit_manually

    # OMFG=(

    * parse posted json dict: {"protocol":int, "datesince":str, "datetill":str}
    * two case:
    * * changes by same date -- write changes into exist snapshot
    * * new date -- make new snap and create new PermitStages (with changes from previous snaps)
    '''
    post = request.POST.items()
    import simplejson
    data = simplejson.loads(str(post[0][0]))
    stagelist_old = StageList.objects.get(pk=permit_id)
    protocol = Protocol.objects.get(pk=int(data['protocol']))

    datesince = data['datesince'].split('.')
    datesince = '%s-%s-%s' % (datesince[2], datesince[1], datesince[0])
    datetill = data['datetill'].split('.')
    datetill ='%s-%s-%s' % (datetill[2], datetill[1], datetill[0])        

    #try:
    if 1==1:
    #    if str(datesince)==str(stagelist_old.date) and protocol==stagelist_old.protocol:
    #        permit = stagelist_old
    #        for permitstage in permit.permitstage_set.all():
    #            permitstage.paused = datetill
    #            permitstage.save()
    #    else:
        permit = Permit(
            orgsro = stagelist_old.orgsro,
            ver = stagelist_old.ver,
            no = stagelist_old.no,
            date = datesince,
            protocol = protocol,
            statement = stagelist_old.statement,
            status = 1
            )
        permit.save()
        log_it(request, permit, ADDITION)

        for permitstage in stagelist_old.permitstage_set.all():
            permitstage = PermitStage(
                stagelist = permit,
                stage = permitstage.stage,
                danger = permitstage.danger,
                paused = datetill
            )
            permitstage.save()

    return HttpResponse(permit.id)

    #except Exception, e:
    #    return HttpResponse(e)

@login_required
#@transaction.commit_manually
def    permit_resume_allstages(request, permit_id):
    '''
    Resuming all stages in permit

    # TODO: return commit_manually

    # OMFG=(

    * parse posted json dict: {"protocol":int}
    * two case:
    * * changes by same date -- write changes into exist snapshot
    * * new date -- make new snap and create new PermitStages (with changes from previous snaps)
    '''
    post = request.POST.items()
    import simplejson
    data = simplejson.loads(str(post[0][0]))
    protocol = Protocol.objects.get(pk=int(data['protocol']))
    stagelist_old = StageList.objects.get(pk=permit_id)

    datesince = data['datesince'].split('.')
    datesince = '%s-%s-%s' % (datesince[2], datesince[1], datesince[0])

    #try:
    if 1==1:
        #if str(datesince)==str(stagelist_old.date) and protocol==stagelist_old.protocol:
        #    permit = stagelist_old
        #    for permitstage in permit.permitstage_set.all():
        #        permitstage.paused = None
        #        permitstage.save()
        #else:
        permit = Permit(
            orgsro = stagelist_old.orgsro,
            ver = stagelist_old.ver,
            no = stagelist_old.no,
            date = datesince,
            protocol = protocol,
            statement = stagelist_old.statement,
            status = 2
            )
        permit.save()
        log_it(request, permit, ADDITION)

        for permitstage in stagelist_old.permitstage_set.all():
            permitstage = PermitStage(
                stagelist = permit,
                stage = permitstage.stage,
                danger = permitstage.danger,
                paused = None
            )
            permitstage.save()

    return HttpResponse(permit.id)

    #except Exception, e:
    #    return HttpResponse(e)

@login_required
def    permit_edit(request, permit_id):
    permit = StageList.objects.get(pk=permit_id)
    if request.method == 'POST':
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            item = form.save()
            log_it(request, permit, CHANGE)
            return HttpResponseRedirect(reverse('sro2.views.permit_view', kwargs={
                'permit_id': permit_id,
                'full': 0,
                'danger' : 0,
            }))
    else:
        form = PermitForm(instance=permit)
    form.setdata(permit.orgsro)
    return render_to_response('sro2/stagelist/stagelist_edit.html', RequestContext(request, { 'form': form, 'stagelist': permit }))

@login_required
@transaction.commit_manually
def    permit_dup(request, permit_id):
    stagelist_old = StageList.objects.get(pk=permit_id)
    if request.method == 'POST':
        form = PermitForm(request.POST)
        if form.is_valid():
            try:
                permit = Permit(
                    orgsro = stagelist_old.orgsro,
                    ver=stagelist_old.ver,
                    no=form.cleaned_data['no'],
                    date=form.cleaned_data['date'],
                    protocol=form.cleaned_data['protocol'],
                    statement=form.cleaned_data['statement']
                    )
                permit.save()

                for ps in stagelist_old.permitstage_set.all():
                    PermitStage(stagelist=permit, stage=ps.stage, danger=ps.danger).save()
            except:
                transaction.rollback()
            #    return HttpResponseRedirect('../../')
            else:
                transaction.commit()
            if (permit.id):
                log_it(request, permit, ADDITION)
                transaction.commit()
            return redirect('sro2.views.stagelist_view',stagelist_id=permit.id, full=0, danger=0)
    else:
        #FIXME!!!
        if stagelist_old.isstatement():
            prevperms=stagelist_old.orgsro.stagelist_set.instance_of(Permit).order_by('permit__date')
            if len(prevperms) > 0:
                prevperm=prevperms[len(prevperms)-1]
                no=prevperm.no
                no=no.replace(' ','')[:-1]+str(int(no.replace(' ','')[-1])+1)
            else:
                no = ''
        else:
            no=stagelist_old.no
        #!!!!!!!!
        form = PermitForm(initial={'statement':permit_id,'no':no})
        form.setdata(stagelist_old.orgsro)
    return render_to_response('sro2/stagelist/stagelist_add.html', RequestContext(request, {'orgsro': stagelist_old.orgsro, 'type': 'Свидетельство', 'form': form}))

@login_required
def    permit_history(request, permit_id):
    '''
    Page with history log -- snaps from this permit

    # TODO: return date ordering
    '''
    permit=Permit.objects.get(pk=permit_id)
    #history=Permit.objects.all().filter(no=permit.no).order_by('date')
    history=Permit.objects.all().filter(no=permit.no,orgsro=permit.orgsro).order_by('id')
    for p in history:
        log = LogEntry.objects.filter(object_id=p.id)
        p.user=log[0].user

    return render_to_response("sro2/stagelist/stagelist_history.html", RequestContext(request, {
        'permit':permit,
        'history':history
    }))

@login_required
def    permit_rollback(request, permit_id, dest_id):
    '''
    Rollback to snap

    # migrate to date filtering

    * del snaps later than this
    '''
    permit=Permit.objects.get(pk=permit_id)
    history=Permit.objects.all().filter(no=permit.no).filter(id__gt=dest_id)
    history.delete()
    return redirect('sro2.views.permit_history',permit_id=permit_id)
