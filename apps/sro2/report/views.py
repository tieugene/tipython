# -*- coding: utf-8 -*-
'''
Orglist views
-------------
'''
from sro2.shared import *
from apps.sro2.models import PermitStage, Permit

@login_required
@render_to('sro2/report.html')
def    report(request):
    '''
    Reports page
    '''
    if_building = False
    if Sro.objects.filter(type__name='Строительство').count() > 0:
        if_building = True
    return {
        'speccase': checkuser_speccase(request.user),
        'if_building': if_building,
    }

@login_required
@render_to('sro2/report/report_brancheslist.html')
def    report_branches_orglist(request):
    '''
    Poor branches org count report

    # !!!DONT USE IT OR REFACTOR!!!
    '''
    branches=[21,32,33,28,23,22]
    orgs=[]
    for branch in branches:
        user=User.objects.get(pk=branch)
        orgs.append({user.last_name:OrgSro.objects.filter(user=branch)})
    return {'orgs': orgs}

@login_required
def    report_statements_list(request):
    '''
    Report for department statistic

    # TODO: make dates changable
    '''
    orgs=OrgSro.objects.all()
    for org in orgs:
        if org.sro.id==1:
            date='2009-09-28'
            org.statements=org.stagelist_set.filter(statement__date__gte=date)
        else:
            date='2010-01-18'
            datesince='2010-08-31'
            org.statements=org.stagelist_set.filter(statement__date__gte=date,statement__date__lte=datesince)
    return render_to_response('sro2/report/report_statements_list.html', RequestContext(request, {'orgs':orgs}))

@login_required
@render_to('sro2/report/report_byuser_list.html')
def    report_byuser_list(request):
    '''
    Report for department statistic

    # TODO: make users changable
    '''
    users=[13,24,3,14,27]
    result=[]
    for user in users:
        user=User.objects.get(pk=user)
        orgs=OrgSro.objects.filter(user=user)
        orgszs=OrgSro.objects.filter(user=user,sro__id=1).count()
        orgsasp=OrgSro.objects.filter(user=user,sro__id=2).count()
        result.append({'user':user,'count':orgs.count(),'countzs':orgszs,'countasp':orgsasp,'orgs':orgs})

    orgs=OrgSro.objects.filter(user=None)
    orgszs=OrgSro.objects.filter(user=None,sro__id=1).count()
    orgsasp=OrgSro.objects.filter(user=None,sro__id=2).count()
    result.append({'user':'','count':orgs.count(),'countzs':orgszs,'countasp':orgsasp,'orgs':orgs})
    branches=[21,32,33,28,23,22]
    bresult=[]
    for user in branches:
        user=User.objects.get(pk=user)
        orgs=OrgSro.objects.filter(user=user)
        orgszs=OrgSro.objects.filter(user=user,sro__id=1).count()
        orgsasp=OrgSro.objects.filter(user=user,sro__id=2).count()
        bresult.append({'user':user,'count':orgs.count(),'countzs':orgszs,'countasp':orgsasp,'orgs':orgs})
    return {'result':result,'bresult':bresult}

@login_required
def    report_orgcount(request):
    orgs=Org.objects.all()
    n=0
    for org in orgs:
        orgsros=OrgSro.objects.filter(org=org).count()
        if orgsros>1 and ((org.user and org.user.id not in [21,32,33,28,23,22]) or not org.user):
            n+=1

    return HttpResponse(n)

@login_required #TODO: right rights
@render_to("sro2/report/report_speclist.html")
def    report_speclist(request):
    '''
    Page with orgs which have speccase status
    '''
    orgs=OrgSro.objects.filter(speccase=True)
    return {'orgs':orgs,'speccase': checkuser_speccase(request.user)}

@login_required
@render_to("sro2/report/report_permit.html")
def    report_permit(request):

    code_list = [32, 33, 8, 22, 25, 26, 27, 28, 29, 30, 31]

    count_general = 0
    permits_general = Permit.objects.filter(~Q(orgsro__org__okopf__name='Индивидуальные предприниматели'),
                                            id__in=PermitStage.objects.filter(~Q(stage__code__in=code_list),
                                                                              stage__parent=None,
                                                                              stage__srotype__name='Строительство',
                                                                              danger=False).distinct().values_list(
                                                    'stagelist__id'))
    for permit in permits_general:
        if permit.orgsro.currperm and permit.orgsro.currperm_id == permit.id:
            count_general += 1

    count_dangerous = 0
    permits_dangerous = Permit.objects.filter(~Q(orgsro__org__okopf__name='Индивидуальные предприниматели'),
                                              id__in=PermitStage.objects.filter(stage__srotype__name='Строительство',
                                                                                danger=True).distinct().values_list(
                                                      'stagelist__id'))
    for permit in permits_dangerous:
        if permit.orgsro.currperm and permit.orgsro.currperm_id == permit.id:
            count_dangerous += 1

    ur = {
        'count_general': count_general,
        'count_dangerous': count_dangerous,
        'count32':get_countofpermits(32),
        'count33':get_countofpermits(33),
        'count8' :get_countofpermits(8),
        'count22':get_countofpermits(22),
        'count25':get_countofpermits(25),
        'count26':get_countofpermits(26),
        'count27':get_countofpermits(27),
        'count28':get_countofpermits(28),
        'count29':get_countofpermits(29),
        'count30':get_countofpermits(30),
        'count31':get_countofpermits(31),
    }

    count_general = 0
    permits_general = Permit.objects.filter(orgsro__org__okopf__name='Индивидуальные предприниматели',
                                            id__in=PermitStage.objects.filter(~Q(stage__code__in=code_list),
                                                                              stage__parent=None,
                                                                              stage__srotype__name='Строительство',
                                                                              danger=False).distinct().values_list(
                                                    'stagelist__id'))
    for permit in permits_general:
        if permit.orgsro.currperm and permit.orgsro.currperm.id == permit.id:
            count_general += 1

    count_dangerous = 0
    permits_dangerous = Permit.objects.filter(orgsro__org__okopf__name='Индивидуальные предприниматели',
                                              id__in=PermitStage.objects.filter(stage__srotype__name='Строительство',
                                                                                danger=True).distinct().values_list(
                                                      'stagelist__id'))
    for permit in permits_dangerous:
        if permit.orgsro.currperm and permit.orgsro.currperm.id == permit.id:
            count_dangerous += 1

    ip = {
        'count_general': count_general,
        'count_dangerous': count_dangerous,
        'count32':get_countofpermits(32, True),
        'count33':get_countofpermits(33, True),
        'count8' :get_countofpermits(8, True),
        'count22':get_countofpermits(22, True),
        'count25':get_countofpermits(25, True),
        'count26':get_countofpermits(26, True),
        'count27':get_countofpermits(27, True),
        'count28':get_countofpermits(28, True),
        'count29':get_countofpermits(29, True),
        'count30':get_countofpermits(30, True),
        'count31':get_countofpermits(31, True),
    }
    return {
        'ur':ur,
        'ip':ip,
        'sros_building': Sro.objects.filter(type__name='Строительство'),
    }

@login_required
@render_to("sro2/report/report_subject.html")
def    report_subject(request):

    data = {}
    for sro in Sro.objects.all():
        okatos = {}
        for okato in Okato.objects.all().order_by('id'):
            ip = OrgSro.objects.filter(org__okopf__name='Индивидуальные предприниматели',sro=sro, org__okato=okato).count()
            ur = OrgSro.objects.filter(~Q(org__okopf__name='Индивидуальные предприниматели'),sro=sro, org__okato=okato).count()
            if ip > 0 or ur > 0:
                okatos[okato] = [ur, ip]
        data[sro] = okatos
    return {
        'data':data,
    }

def    get_countofpermits(stage_code, ip=False):

    count = 0

    if ip:
        permits = Permit.objects.filter(orgsro__org__okopf__name='Индивидуальные предприниматели',
                                        id__in=PermitStage.objects.filter(stage__srotype__name='Строительство',
                                                                          stage__code=stage_code).distinct().values_list(
                                                'stagelist__id'))
    else:
        permits = Permit.objects.filter(~Q(orgsro__org__okopf__name='Индивидуальные предприниматели'),
                                        id__in=PermitStage.objects.filter(stage__srotype__name='Строительство',
                                                                          stage__code=stage_code).distinct().values_list(
                                                'stagelist__id'))

    for permit in permits:
        if permit.orgsro.currperm and permit.orgsro.currperm.id == permit.id:
            count += 1

    return count