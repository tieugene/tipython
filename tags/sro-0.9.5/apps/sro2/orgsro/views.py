# -*- coding: utf-8 -*-
'''
OrgSro views
----------
'''
from sro2.shared import *
from datetime import  date
from gw.forms import ContactAddressTypeForm

@login_required
def    orgsro_del(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    sro_id = orgsro.sro.id
    org = orgsro.org
    #log_it(request, orgsro, DELETION)
    orgsro.delete()
    if (org.orgsro_set.all().count() == 0):
        #log_it(request, org, DELETION)
        org.delete()
    #return HttpResponseRedirect(reverse('sro2.views.sro_list', kwargs={'sro_id': sro_id}))
    return redirect('sro2.orglist.views.orglist_list',sro_id=sro_id)

@login_required
@render_to('sro2/orgsro/orgsro_view.html')
def    orgsro_view(request, orgsro_id = None, sro_id = None, org_id = None):
    if sro_id is None:
        orgsro = OrgSro.objects.get(pk=orgsro_id)
        sro = orgsro.sro
        org = orgsro.org
    else:
        org = Org.objects.get(pk=org_id)
        sro = Sro.objects.get(pk=sro_id)
        orgsro = OrgSro.objects.get(org=org, sro=sro)

    personsro_list = sro.personorgsro_set.filter(org=org).values_list('person')
    person_list = org.orgstuff_set.filter(person__in=personsro_list,enddate__isnull=True).order_by('-leader', 'person')
    statements=orgsro.stagelist_set.instance_of(Statement).order_by('statement__date')

    #FIXME.
    #hz why i need do it=(
    try:
        orglicense=OrgLicense.objects.filter(orgsro=orgsro)
    except:
        orglicense=False

    hist=History(orgsro)
    permits = hist.originals()

    for perm in permits:
        try:
            perm.last=hist.last_snap(perm)
        except:
            perm.last=''

    reasons=Reason.objects.all()
    form=ProtocolListForm()
    form.setdata(orgsro)
    for pers in person_list:
        pers.skill=get_skill(pers.person.id)
    insurance=OrgInsurance.objects.filter(orgsro=orgsro)
    
    formaddresstype = ContactAddressTypeForm()
    formaddresstype.setdata(org.id)
    if formaddresstype.fields['type'].queryset.count() > 0:
        show_add_address = True
    else:
        show_add_address = False

    return {
        'orgsro': orgsro,
        'canedit': checkuser(orgsro.org, request.user),
        'canedit_orgsro': checkuser(orgsro, request.user),
        'person_list': person_list,
        'statements':statements,
        'permits':permits,
        'reasons':reasons,
        'p_form':form,
        'speccase': checkuser_speccase(request.user),
        'insurance':insurance,
        'show_button_address': show_add_address,
        'orglicense':orglicense,
    }

@login_required
def    orgsro_certificate(request, orgsro_id):
    '''FIXME'''
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    data = dict()
    data['orgsro'] = orgsro
    data['date'] = strdate(orgsro.regdate)
    data['bigdate'] = strdate(orgsro.regdate).upper()
    return pdf_render_to_response(os.path.join('sro2', 'cert_%s.rml' % orgsro.sro.sroown.tplprefix), {'data': data}, filename=str(orgsro.regno) + '.pdf')

@login_required
def    orgsro_extract(request, orgsro_id,full):
    '''
    Extract (выписка из реестра). Main information + permits history

    * get permits
    * fix snapshot data to original
    * get history
    * get original of previous permits (first by date in unique numbers of permit)
    '''
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    stagelists = StageList.objects.instance_of(Permit).filter(orgsro=orgsro, permit__date__lte=datetime.today())
    permit =orgsro.currperm
    hist=History(orgsro)
    history=hist.get_history()
    prevs=hist.prevs()
    insurance=OrgInsurance.objects.filter(orgsro=orgsro,active=True)
    lasthist=''
    if permit:
        lasthist={'desc':'<b>Свидетельство №%s от %s (%s) - Действующее:' % (permit.no,strdatedot(permit.date),permit.protocol.asstr_full())}
    if history:
        lasthist=history[-1]
    tpl=orgsro.sro.sroown.tplprefix
    footer=''
    if int(full):
        tpl+='_full'
    kf=int(orgsro.paysum)
    ins=0
    for i in insurance:
        ins+=int(i.sum)
    if orgsro.sro.id==2 and orgsro.currperm.stages.filter(code='13').count():
        if kf>=150000 and ins>=5000000:
            footer='Допуск к работам по организации подготовки проектной документации выдан для выполнения работ по организации подготовки проектной документации, стоимость которой по одному договору не превышает пять миллионов рублей (п.1, ч.6, ст.55.16 ГрК РФ)'
        if kf>=250000 and ins>=10000000:
            footer='Допуск к работам по организации подготовки проектной документации выдан для выполнения работ по организации подготовки проектной документации, стоимость которой по одному договору не превышает двадцать пять миллионов рублей (п.2, ч.6, ст.55.16 ГрК РФ)'
        if kf>=500000 and ins>=35000000:
            footer='Допуск к работам по организации подготовки проектной документации выдан для выполнения работ по организации подготовки проектной документации, стоимость которой по одному договору не превышает пятьдесят миллионов рублей (п.3, ч.6, ст.55.16 ГрК РФ)'
        if kf>=1000000 and ins>=100000000:
            footer='Допуск к работам по организации подготовки проектной документации выдан для выполнения работ по организации подготовки проектной документации, стоимость которой по одному договору не превышает трехсот миллионов рублей (п.4, ч.6, ст.55.16 ГрК РФ)'
        if kf>=1500000 and ins>=120000000:
            footer='Допуск к работам по организации подготовки проектной документации выдан для выполнения работ по организации подготовки проектной документации, стоимость которой по одному договору составляет триста миллионов рублей и более (п.5, ч.6, ст.55.16 ГрК РФ)'
    elif orgsro.sro.id==1 and orgsro.currperm.stages.filter(code='33').count():
        if kf>=300000 and ins>=10000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору не превышает десять миллионов рублей (п.1, ч.7, ст.55.16 ГрК РФ)'
        if kf>=500000 and ins>=20000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору не превышает шестьдесят миллионов рублей (п.2, ч.7, ст.55.16 ГрК РФ)'
        if kf>=1000000 and ins>=30000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору не превышает пятьсот миллионов рублей (п.3, ч.7, ст.55.16 ГрК РФ)'
        if kf>=2000000 and ins>=100000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору не превышает три миллиарда рублей (п.4, ч.7, ст.55.16 ГрК РФ)'
        if kf>=3000000 and ins>=200000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору не превышает десять миллиардов рублей (п.5, ч.7, ст.55.16 ГрК РФ)'
        if kf>=10000000 and ins>=300000000:
            footer='Допуск к работам по организации строительства выдан для выполнения работ по организации строительства, стоимость которого по одному договору составляет десять миллиардов рублей и более (п.6, ч.7, ст.55.16 ГрК РФ)'

    return jrender_to_response(os.path.join('sro2', 'extract_%s.html' % tpl), { 'orgsro': orgsro, 'permit': permit, 'history':history, 'date': datetime.now(),'prevs':prevs,'lasthist':lasthist,'insurance':insurance,'tpl':tpl,'footer':footer})

@login_required
@render_to('sro2/orgsro/orgsro_org.html')
def    orgsro_org_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    org = orgsro.org
    if request.method == 'POST':
        form = OrgEditForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save()
            #log_it(request, org, CHANGE)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
            return redirect(orgsro_view,orgsro_id=orgsro.id)
    else:
        form = OrgEditForm(instance=org)
        okopf = Okopf.objects.all()
    return {'orgsro': orgsro, 'form': form}

@login_required
@render_to('sro2/orgsro/orgsro_main.html')
def    orgsro_main_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = OrgSroForm(request.POST, instance=orgsro)
        if form.is_valid():
            orgsro = form.save()
            #log_it(request, orgsro, CHANGE)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
            return redirect(orgsro_view,orgsro_id=orgsro.id)
    else:
        form = OrgSroForm(instance=orgsro)

    insurance=OrgInsurance.objects.filter(orgsro=orgsro,active=True)
    return {'orgsro': orgsro, 'form': form,'insurance':insurance}

@login_required
@render_to('sro2/orgsro/orgsro_license.html')
def    orgsro_license_add(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = OrgLicenseForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.orgsro = orgsro
            new_item.save()
            #log_it(request, new_item, ADDITION)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
            return redirect(orgsro_view,orgsro_id=orgsro.id)
    else:
        form = OrgLicenseForm()
    return {'orgsro': orgsro, 'form': form}

@login_required
@render_to('sro2/orgsro/orgsro_license.html')
def    orgsro_license_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    item = orgsro.orglicense
    if request.method == 'POST':
        form = OrgLicenseForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, CHANGE)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
            return redirect(orgsro_view,orgsro_id=orgsro.id)
    else:
        form = OrgLicenseForm(instance=item)
    return {'orgsro': orgsro, 'form': form}

@login_required
def    orgsro_license_del(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    item = orgsro.orglicense
    #log_it(request, item, DELETION)
    item.delete()
    #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
    return redirect(orgsro_view,orgsro_id=orgsro.id)

@login_required
@render_to('sro2/orgsro/orgsro_insurance.html')
def    orgsro_insurance_add(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = OrgInsuranceForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.orgsro = orgsro
            new_item.save()
            #log_it(request, new_item, ADDITION)
            return redirect(orgsro_view,orgsro_id=orgsro.id)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
    else:
        form = OrgInsuranceForm()
    return {'orgsro': orgsro, 'form': form}

@login_required
@render_to('sro2/orgsro/orgsro_insurance.html')
def    orgsro_insurance_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    item=OrgInsurance.objects.filter(orgsro=orgsro).latest("date")
    if request.method == 'POST':
        form = OrgInsuranceForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, CHANGE)
            return redirect(orgsro_view,orgsro_id=orgsro.id)
    else:
        form = OrgInsuranceForm(instance=item)
    return {'orgsro': orgsro, 'form': form}

@login_required
def    orgsro_insurance_del(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    item=OrgInsurance.objects.filter(orgsro=orgsro).latest("date")
    #log_it(request, item, DELETION)
    item.delete()
    return redirect(orgsro_view,orgsro_id=orgsro.id)

@login_required
@render_to('sro2/orgsro/orgsro_okved.html')
def    orgsro_okved_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':    # add
        item = OrgOkved(org=orgsro.org, okved=Okved.objects.get(pk=request.POST['okved']))
        item.save()
        #log_it(request, item, CHANGE)
    return {'orgsro': orgsro, 'okved': Okved.objects.all()}

@login_required
def    orgsro_okved_del(request, orgsro_id, item_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    item = OrgOkved.objects.get(pk=item_id)
    #log_it(request, item, DELETION)
    item.delete()
    return redirect(orgsro_okved_edit,orgsro_id=orgsro.id)


@login_required
@render_to('sro2/orgsro/orgsro_stuff.html')
def    orgsro_stuff_edit(request, orgsro_id = None):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    org = orgsro.org
    sro = orgsro.sro

    form = OrgStuffForm_Soft(org)
    if 'person_id' in request.GET:
       form.initial = {
            'person': int(request.GET['person_id']),
        }

    personsro_list = sro.personorgsro_set.filter(org=org).values_list('person')
    person_list = org.orgstuff_set.filter(person__in=personsro_list).order_by('enddate','-leader', 'person')
    for pers in person_list:
        pers.skill=get_skill(pers.person.id)

    person_list_org = org.orgstuff_set.filter(~Q(person__in=personsro_list)).order_by('enddate','-leader', 'person')
    for pers in person_list_org:
        pers.skill=get_skill(pers.person.id)

    if 'orgstuff_id' in request.GET: # by editing OrgStuff
        orgstuff_id = int(request.GET['orgstuff_id'])
        orgstuff = OrgStuff.objects.get(pk=orgstuff_id)
        form_orgstuff_edit = OrgStuffForm()
        form_orgstuff_edit.initial = {
            'role': orgstuff.role.id,
            'leader': orgstuff.leader,
            'permanent': orgstuff.permanent,
            'startdate': orgstuff.startdate,
        }

        return {
            'orgsro': orgsro,
            'form': form,
            'form_person': OrgStuffAddPersonForm(),
            'form_role': OrgStuffAddRoleForm(),
            'person_list': person_list,
            'person_list_org': person_list_org,
            'form_orgstuff_edit': form_orgstuff_edit,
            'orgstuff_id': orgstuff_id,
        }

    return {
        'orgsro': orgsro,
        'form': form,
        'form_person': OrgStuffAddPersonForm(),
        'form_role': OrgStuffAddRoleForm(),
        'person_list': person_list,
        'person_list_org': person_list_org,
    }

@login_required
def    orgsro_stuff_orgstuff_add(request, orgsro_id = None):

    orgsro = OrgSro.objects.get(pk=orgsro_id)

    if request.method == 'POST':
        form = OrgStuffForm(request.POST)

        if form.is_valid():
            #return HttpResponse(form.is_valid())
            new_item = form.save(commit=False)
            new_item.org = orgsro.org
            new_item.save()
            #log_it(request, new_item, CHANGE)
            person = new_item.person
            item = PersonOrgSro.objects.create(person=person,org=orgsro.org,sro=orgsro.sro)
            #log_it(request, item, ADDITION)
            form = OrgStuffForm_Soft(orgsro.org)

    return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}))
    #return HttpResponse(form.is_valid())

@login_required
@render_to('sro2/orgsro/stuff_table.html')
def    orgsro_stuff_table(request, orgsro_id):

    orgsro = OrgSro.objects.get(pk=orgsro_id)
    sro = orgsro.sro
    org = orgsro.org

    personsro_list = sro.personorgsro_set.filter(org=org).values_list('person')
    person_list = org.orgstuff_set.filter(person__in=personsro_list).order_by('-leader', 'person')

    return {
        'orgsro': orgsro,
        'person_list': person_list,
    }

@login_required
def    orgsro_stuff_add_person(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = OrgStuffAddPersonForm(request.POST)
        if form.is_valid():
            item = form.save()
            item.user=request.user
            item.save()
            #log_it(request, item, ADDITION)
    return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}) + '?person_id=%d' % item.id)

@login_required
def    orgsro_stuff_add_role(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        form = OrgStuffAddRoleForm(request.POST)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, ADDITION)
            return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}) + '?role=%d' % item.id)
        return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def    orgsro_stuff_del(request, orgsro_id, item_id):
    orgstuff = OrgStuff.objects.get(pk=item_id)
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    sro = orgsro.sro
    org = orgsro.org
    person = orgstuff.person

    try:
        personorgsro = PersonOrgSro.objects.get(org=org, person=person, sro=sro)
        #log_it(request, personorgsro, DELETION)
        personorgsro.delete()

        if (person.personorgsro_set.filter(org=org).count() == 0):
            #log_it(request, orgstuff, DELETION)
            orgstuff.delete()
    except:
        pass

    return redirect(orgsro_stuff_edit,orgsro_id=orgsro.id)

@login_required
def    orgsro_stuff_return(request, orgsro_id, item_id):
    orgstuff = OrgStuff.objects.get(pk=item_id)
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    orgstuff.enddate=None
    orgstuff.save()
    return redirect(orgsro_stuff_edit,orgsro_id=orgsro.id)

@login_required
def    orgsro_stuff_dismiss(request, orgsro_id, item_id,enddate):
    orgstuff = OrgStuff.objects.get(pk=item_id)
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    #sro = orgsro.sro
    #org = orgsro.org
    #person = orgstuff.person
    from datetime import date
    eday,emounth,eyear = enddate.split('.')
    ed=date(int(eyear), int(emounth), int(eday))
    orgstuff.enddate=ed
    orgstuff.save()
    return redirect(orgsro_stuff_edit,orgsro_id=orgsro.id)

@login_required
def    orgsro_stuff_add_exist(request, orgsro_id, item_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    org = orgsro.org
    sro = orgsro.sro
    person = Person.objects.get(pk=item_id)
    try:
        if request.method == 'POST':
            item = PersonOrgSro.objects.create(person=person,org=org,sro=sro)
            #log_it(request, item, ADDITION)
    except:
        pass
    return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}) + '?person=%d' % item.id)

@login_required
def    orgsro_stuff_orgstuff_edit(request, orgsro_id, orgstuff_id):

    orgsro = OrgSro.objects.get(pk=orgsro_id)
    orgstuff = OrgStuff.objects.get(pk=orgstuff_id)
    role = Role.objects.get(pk=request.POST['role'])

    if request.POST['startdate']:
        d,m,y = request.POST['startdate'].split('.')
        startdate = date(int(y), int(m), int(d))
    else:
        startdate = None

    if 'leader' in request.POST:
        leader = 1
    else:
        leader = 0
    if 'permanent' in request.POST:
        permanent = 1
    else:
        permanent = 0

    orgstuff.role = role
    orgstuff.leader = leader
    orgstuff.permanent = permanent
    orgstuff.startdate = startdate
    orgstuff.save()
    #log_it(request, orgstuff, CHANGE)

    return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={
        'orgsro_id': orgsro.id
    }))

@login_required
def    orgsro_event_edit(request, orgsro_id):
    return render_to_response('sro2/orgsro/dummy.html')

@login_required
def    orgsro_event_del(request, orgsro_id, item_id):
    return HttpResponseRedirect('sro2/orgsro/dummy.html')

@login_required
def    orgsro_to_candidate(request, orgsro_id):
    '''
    Return member org to candidate

    # promote to candidate -- goto orgsro_statement_add
    '''
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    try:
        orgsro.regno=None
        orgsro.regdate=None
        orgsro.status=1
        orgsro.save()
        #log_it(request, orgsro, CHANGE, u'Статус')
        return redirect(orgsro_view,orgsro_id=orgsro_id)
    except Exception,e:
        return HttpResponse(e)

@login_required
def    orgsro_to_archive(request, orgsro_id):
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    try:
        orgsro.status=4
        orgsro.save()
        #log_it(request, orgsro, CHANGE, u'Статус')
        return redirect(orgsro_view,orgsro_id=orgsro_id)
    except Exception,e:
        return HttpResponse(e)

@login_required
def    orgsro_to_member(request, orgsro_id):
    '''
    Promote candidate to member
    '''
    post=request.POST.items()
    import simplejson
    regs=simplejson.loads(str(post[0][0]))
    regno=regs['regno']
    inprotocol=regs['protocol']
    regdate=regs['regdate']
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    try:
        orgsro.regno=regno
        regdate=regdate.split('.')
        orgsro.regdate='%s-%s-%s' % (regdate[2],regdate[1],regdate[0])
        orgsro.status=2
        orgsro.inprotocol=Protocol.objects.get(pk=inprotocol)
        orgsro.save()
        #log_it(request, orgsro, CHANGE, u'Статус')
        return HttpResponse('Success')
    except Exception,e:
        return HttpResponse(e)

@login_required
def    orgsro_to_excluded(request, orgsro_id):
    '''
    Exclude member from Sro
    '''
    post=request.POST.items()
    import simplejson
    ex=simplejson.loads(str(post[0][0]))
    reasons=ex['reason']
    exprotocol=ex['protocol']
    excludedate=ex['excludedate']
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    #try:
    for reason in reasons:
        orgreason=OrgReason(orgsro=orgsro,reason=Reason.objects.get(pk=int(reason)))
        orgreason.save()
    exdate=excludedate.split('.')
    orgsro.excludedate='%s-%s-%s' % (exdate[2],exdate[1],exdate[0])
    orgsro.status=3
    if exprotocol:
        orgsro.exprotocol=Protocol.objects.get(pk=int(exprotocol))
    orgsro.save()
    #log_it(request, orgsro, CHANGE, u'Статус')
    return HttpResponse('Success')

@login_required
def    orgsro_return_member(request, orgsro_id):
    '''
    Return excluded org to member
    '''
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    try:
        for r in orgsro.orgreason_set.all():
            r.delete()
        orgsro.excludedate=None
        orgsro.status=2
        orgsro.save()
        #log_it(request, orgsro, CHANGE, u'Статус')
        return redirect(orgsro_view,orgsro_id=orgsro_id)
    except Exception,e:
        return HttpResponse(e)

@login_required
@render_to('sro2/orgsro/orgsro_stagelist.html')
def    orgsro_stagelist_edit(request, orgsro_id):
    orgsro = OrgSro.objects.get(pk=orgsro_id)
    if request.method == 'POST':
        if request.POST['type_id']:
            if request.POST['type_id'] == 'statement':
                return HttpResponseRedirect(reverse('sro2.views.statement_add', kwargs={'orgsro_id': orgsro.id}))
            elif request.POST['type_id'] == 'permit':
                return HttpResponseRedirect(reverse('sro2.views.permit_add', kwargs={'orgsro_id': orgsro.id}))
            else:
                return HttpResponseRedirect(reverse('sro2.views.alienpermit_add', kwargs={'orgsro_id': orgsro.id}))

    permits = orgsro.stagelist_set.instance_of(Permit).order_by('permit__date')
    statements = orgsro.stagelist_set.instance_of(Statement).order_by('statement__date')

    nos=[]
    for perm in permits:
        if perm.no not in nos:
            nos.append(perm.no)
    prevs=[]
    for num in nos:
        l=Permit.objects.all().filter(no=num,orgsro=orgsro).order_by('date')
        prevs.append(l[0])
    return {'orgsro': orgsro, 'permits':prevs, 'statements':statements}


@render_to('sro2/orgsro/org_view.html')
def org_view(request,org_id):
    orgsros=OrgSro.objects.filter(org__id=org_id)
    if orgsros.count()==1:
        return redirect(orgsro_view,orgsro_id=orgsros[0].id)
    else:
        return {'orgsros':orgsros}



def    get_skill(person_id):
    '''
    Get person skill function

    * format string from _all_ person skills with seniority and skill grade
    '''
    skill=''
    person = PersonSkill.objects.all().filter(person=person_id)
    if person.count>1:
        for item in person:
            if item.skill.high:
                skill_high=' (высшее)'
            else:
                skill_high=''
            skill='%s, %s (Стаж: %s), %s%s' % (skill,item.speciality.name,item.seniority,item.skill.name,skill_high)
        skill=skill[2:]
    else:
        skill='%s (Стаж: %s)' % (person.speciality.name,item.seniority)
    if not skill:
        skill='Специальность не указана.'
    return skill

@login_required
def    orgsro_spec_edit(request, orgsro_id):
    '''
    Edit special comments
    '''
    post=request.POST.items()
    import simplejson
    specs=simplejson.loads(str(post[0][0]))
    speccase=specs['speccase']
    speccomments=specs['speccomments']
    orgsro=OrgSro.objects.get(pk=orgsro_id)
    try:
        orgsro.speccase=speccase
        orgsro.speccomments=speccomments
        orgsro.save()
        return HttpResponse('Success')
    except Exception,e:
        return HttpResponse(e)



@login_required #TODO: right rights
def    orgsro_spec_del(request,orgsro_id):
    '''
    Delete speccase status and comments
    '''
    org=OrgSro.objects.get(pk=orgsro_id)
    org.speccase=False
    org.speccomments=None
    org.save()
    return redirect('sro2.report.views.report_speclist')


