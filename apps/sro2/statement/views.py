# -*- coding: utf-8 -*-
'''
Statement views
----------
'''

from sro2.shared import *
from django.db.models import Q

@login_required
def    statement_view(request, statement_id, full, danger):
    '''
    Statement view-sorter
    '''
    stagelist = StageList.objects.get(pk=statement_id)
    full = int(full)
    danger = int(danger)

    if not full:
        return jrender_to_response('sro2/stagelist/stagelist_view.html', {
            'stagelist': stagelist,
            'itemlist': stagelist.permitstage_set.dict(danger),
            'canedit': checkuser(stagelist.orgsro.org, request.user),
            'canedit_orgsro': checkuser(stagelist.orgsro, request.user),
            'danger': int(danger),
            'full': 0,
        },request)
    else:
        return jrender_to_response('sro2/stagelist/stagelist_full.html', {
            'stagelist': stagelist,
            'itemlist': stagelist.permitstage_set.dict_extra(stagelist, danger),
            'canedit': checkuser(stagelist.orgsro.org, request.user),
            'canedit_orgsro': checkuser(stagelist.orgsro, request.user),
            'danger': int(danger),
            'full': 1
        },request)

@login_required
def    statement_link(request, statement_id, permit_id):
    try:
        statement=Statement.objects.get(pk=statement_id)
        permit=Permit.objects.get(pk=permit_id)
        permit.statement=statement
        permit.save()
        return HttpResponse('Success')
    except Exception,e:
        return HttpResponse(e)

@login_required
def    statement_add(request, orgsro_id):
    '''
    Add new statement
    '''
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = StatementAddForm(request.POST)
        if form.is_valid():
            try:
                statement = Statement(
                    date=form.cleaned_data['date'],
                    orgsro=orgsro,
                    ver=form.cleaned_data['ver']
                )
                if not len(orgsro.stagelist_set.instance_of(Statement).all()):
                    orgsro.status=1
                    orgsro.save()
                statement.save()
            except:
                transaction.rollback()
            else:
                transaction.commit()
            if (statement.id):
                #log_it(request, statement, ADDITION)
                transaction.commit()
            return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={'orgsro_id': orgsro.id}))
    else:
        form = StatementAddForm()
#        form.setdata(orgsro)
#        permitform =PermitListForm()
#        permitform.setdata(orgsro)
    return jrender_to_response('sro2/stagelist/stagelist_add.html', {'orgsro': orgsro, 'form': form, 'type': 'Заявление'},request)

@login_required
def    statement_attachment_pdf(request, statement_id):
    '''
    Print statement attachment
    '''

    from datetime import datetime, date, time, timedelta
    statement = Statement.objects.get(pk=statement_id)
    orgsro = statement.orgsro
    min_date = Statement.objects.filter(orgsro=orgsro).aggregate(Min('date'))['date__min']
    filename = 'statement_' + orgsro.sro.sroown.tplprefix + '_' + statement.date.strftime("%d-%m-%Y") + '.pdf'

    stages = Stage.objects.filter(ver = statement.ver, srotype = orgsro.sro.type).distinct().order_by('id')

    if (min_date == statement.date): # это заявление для вступления
        change = False
    else: # это заявление для внесения изменений
        change = True

    if statement.ver.id == 2 or statement.date >= date(2009,12,31): # 4-я версия или 3-я версия

        if statement.ver.id == 2: # 4-я версия
            ver = 4
        else: # 3-я версия
            ver = 3

        if (orgsro.sro.id == 1) and (ver != 4): # МООЖС
            stages = stages.filter(parent=None)

        if not change: # это заявление для вступления

            template_name = os.path.join('sro2', 'statement_attachment/%s_ver34_entry.rml' % orgsro.sro.sroown.tplprefix)
            stages_o = statement.stages.filter(permitstage__danger = False)
            stages_d = statement.stages.filter(permitstage__danger = True)
            o = set(stages_o.values_list('id', flat=True))
            d = set(stages_d.values_list('id', flat=True))
            data = {
                'statement': statement,
                'stages': stages,
                'o': o,
                'd': d,
                'date': strdate(statement.date),
                'user': request.user.username,
                'change': change,
                'ver': ver,
                'type_changed': False,
            }

            return pdf_render_to_response(template_name, {'data': data}, filename=filename)

        else: # это заявление для внесения изменений

            date_prev_statement = Statement.objects.filter(orgsro=orgsro, date__lt=statement.date).aggregate(Max('date'))['date__max']
            prev_statement = Statement.objects.get(orgsro=orgsro,date=date_prev_statement)
            template_name = os.path.join('sro2', 'statement_attachment/%s_ver34_change.rml' % orgsro.sro.sroown.tplprefix)

            if statement.ver.id == prev_statement.ver.id:
                type_changed = False
                
                h = History(orgsro)
                deleted, added, common = h.cmp_stagelists(prev_statement, statement, True)

                permitstages_o_del = deleted.filter(danger = False)
                permitstages_o_add = added.filter(danger = False)

                permitstages_d_del = deleted.filter(danger = True)
                permitstages_d_add = added.filter(danger = True)

                d_del = set(permitstages_d_del.values_list('stage__id', flat=True))
                o_del = set(permitstages_o_del.values_list('stage__id', flat=True))
                
                count_o_del = permitstages_o_del.filter(Q(stage__parent=True)|Q(stage__isgroup=False)).count()
                count_d_del = permitstages_d_del.filter(Q(stage__parent=True)|Q(stage__isgroup=False)).count()            

            else: #  previous statement has older type of stages's list then current statement
                type_changed = True
                permitstages = statement.permitstage_set.all()

                for permitstage in permitstages.filter(stage__isgroup=True):
                    permitstage_list = permitstages.filter(danger=permitstage.danger, stage__parent=permitstage.stage)
                    if permitstage.danger:
                        stage_list = Stage.objects.filter(parent=permitstage.stage)
                    else:
                        stage_list = Stage.objects.filter(parent=permitstage.stage, dangeronly=False)
                    if permitstage_list.count() != stage_list.count():
                        permitstages = permitstages.exclude(id=permitstage.id)

                permitstages_o_add = permitstages.filter(danger = False)
                permitstages_d_add = permitstages.filter(danger = True)
                d_del = set()
                o_del = set()
                count_o_del = 0
                count_d_del = 0
            
            count_o_add = permitstages_o_add.filter(Q(stage__parent=True)|Q(stage__isgroup=False)).count()
            count_d_add = permitstages_d_add.filter(Q(stage__parent=True)|Q(stage__isgroup=False)).count()
            
            o_add = set(permitstages_o_add.values_list('stage__id', flat=True))
            d_add = set(permitstages_d_add.values_list('stage__id', flat=True))

            data = {
                'statement': statement,
                'stages': stages,
                'o_del': o_del,
                'count_o_del': count_o_del,
                'o_add': o_add,
                'count_o_add': count_o_add,
                'd_del': d_del,
                'count_d_del': count_d_del,
                'd_add': d_add,
                'count_d_add': count_d_add,
                'date': strdate(statement.date),
                'user': request.user.username,
                'change': change,
                'ver': ver,
                'type_changed': type_changed,
            }

            return pdf_render_to_response(template_name, {'data': data}, filename=filename)


    else: # 1-я версия

        if orgsro.sro.id == 1: # МООЖС
            stages = stages.exclude(Q(code='36')|Q(code='37')|Q(code='38'))
            stages = stages.filter(parent=None)
            count_genpodryad = statement.stages.filter(Q(code='36')|Q(code='37')|Q(code='38')).count()
        elif orgsro.sro.id == 2: # МООАСП
            stages = stages.exclude(Q(code='13')|Q(code='14'))
            count_genpodryad = statement.stages.filter(Q(code='13')|Q(code='14')).count()

        count_danger = statement.stages.filter(permitstage__danger = True).count()

        ver = 1
        template_name = os.path.join('sro2', 'statement_attachment/%s_ver1.rml' % orgsro.sro.sroown.tplprefix)
        stages_o = statement.stages.filter(permitstage__danger = False)
        o = set(stages_o.values_list('id', flat=True))
        data = {
            'statement': statement,
            'stages': stages,
            'o': o,
            'date': strdate(statement.date),
            'user': request.user.username,
            'change': change,
            'ver': ver,
            'stages_o': stages_o,
            'type_changed': False,
            'incorrect_stages': (count_genpodryad > 0 or count_danger > 0),
        }

        return pdf_render_to_response(template_name, {'data': data}, filename=filename)

@login_required
def    statement_del(request, statement_id):
    '''
    Del statement
    '''

    statement = StageList.objects.get(pk=statement_id)
    orgsro_id = statement.orgsro.id

    try:
        # clearing the value of the field "statement" for corresponing models "Permit" before deleting statement
        permit_list = Permit.objects.filter(statement__id=statement.id)
        for permit in permit_list:
            #log_it(request, permit, CHANGE)
            permit.statement = None
            permit.save()

        #log_it(request, statement, DELETION)
        statement.delete()

    except:
        pass

    return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={'orgsro_id': orgsro_id}))

@login_required
@render_to('sro2/stagelist/stagelist_edit.html')
def    statement_edit(request, statement_id):
    '''
    Edit existent statement
    '''

    statement = StageList.objects.get(pk=statement_id)

    if request.method == 'POST':
        form = StatementForm(request.POST, instance=statement)
        if form.is_valid():
            item = form.save()
            #log_it(request, statement, CHANGE)
            return redirect('sro2.views.statement_view',statement_id=statement.id,full=0,danger=0)
    else:
        form = StatementForm(instance=statement)
        form.fields['rejectprotocol'].queryset = Protocol.objects.filter(sro=statement.orgsro.sro)
        protocolform = ProtocolListForm()
        protocolform.setdata(statement.orgsro)
        permitform =PermitListForm()
        permitform.setdata(statement.orgsro)
    return { 'form': form, 'stagelist': statement,"protocolform":protocolform,'permitform':permitform }

@login_required
@transaction.commit_manually
def    statement_dup(request, statement_id):
    '''
    Make dub[p]licate
    '''
    stagelist_old = StageList.objects.get(pk=statement_id)
    if request.method == 'POST':
        form = StatementForm(request.POST)
        if form.is_valid():
            try:
                statement = Statement(
                    orgsro=stagelist_old.orgsro,
                    ver=stagelist_old.ver,
                    date=form.cleaned_data['date']
                )
                statement.save()

                for ps in stagelist_old.permitstage_set.all():
                    PermitStage(stagelist=statement, stage=ps.stage, danger=ps.danger).save()
            except:
                transaction.rollback()
            #    return HttpResponseRedirect('../../')
            else:
                transaction.commit()
            if (statement.id):
                #log_it(request, statement, ADDITION)
                transaction.commit()
                return HttpResponseRedirect(reverse('sro2.views.statement_view', kwargs={
                    'statement_id': statement.id,
                    'full': 0,
                    'danger': 0,
                }))
    else:
        form = StatementForm()
    return jrender_to_response('sro2/stagelist/stagelist_add.html', {'orgsro': stagelist_old.orgsro, 'type': 'Заявление', 'form': form},request)

@login_required
@transaction.commit_manually
def    permit_dup_edit(request, permit_id):
    '''
    Edit new dup
    '''
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
                #log_it(request, permit, ADDITION)
                transaction.commit()
            return redirect(statement_view,statement_id=permit.id,full=0,danger=0)
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

