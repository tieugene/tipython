# -*- coding: utf-8 -*-
'''
Orglist views
----------
'''
from sro2.shared import *
import sys, ftplib, netrc, tempfile, csv, pprint, itertools, tarfile, time
from paramiko import SSHClient, AutoAddPolicy

@login_required
@render_to('sro2/orglist/orgtable.html')
def    orglist_list_get(request,sro_id):
    '''
    Post organisations list to ajax. Use only on plain get (without filters).
    '''
    sro = Sro.objects.get(pk=sro_id)
    orgsro_list = sro.orgsro_set.select_related('org__name',).order_by('org__name')
    return {'sro': sro,'list': orgsro_list,}

@login_required
@render_to('sro2/orglist/orglist_orglist.html')
def    orglist_list(request, sro_id, page_num):
    '''
    Organisation list. Filters with OKATO and Insurer
    '''
    sro = Sro.objects.get(pk=sro_id)
    stage=''
    filtr={}
    count=0
    orgsro_list={}
    if request.method == 'POST' and request.POST:
        orgsro_list = sro.orgsro_set.select_related('org__name',).order_by('org__name')
        if (request.POST['okato']):
            orgsro_list = orgsro_list.filter(org__okato__pk=request.POST['okato'])
            okato=Okato.objects.get(pk=request.POST['okato']).name
            filtr={'name':'ОКАТО','value':okato}
            count=len(orgsro_list)
        elif (request.POST['insurer']):
#FIXME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# result include _ALL_ insurences. fix it.
            orgsro_list = orgsro_list.filter(orginsurance__insurer__pk=request.POST['insurer'])
            insurer=Insurer.objects.get(pk=request.POST['insurer']).name
            filtr={'name':'Страхователь','value':insurer}
            count=len(orgsro_list)
        if not orgsro_list:
            orgsro_list=[]
            orgsro_list.append(OrgSro.objects.get(pk=831))

    formaddexist = OrgAddExistsForm(sro)
    return {
        'sro': sro,
        'list': orgsro_list,
        'form': OrgListForm(),
        'formaddexist': formaddexist,
        'filtr':filtr,
        'count':count,
    }

@login_required
@render_to('sro2/orglist/orglist_memberlist.html')
def    orglist_publish(request, sro_id):
    '''
    @param sro_id:int - Sro.id
    '''
    sro = Sro.objects.get(pk=sro_id)
    return {
        'sro': sro,
        'item_list': sro.orgsro_set.filter(publish=True, status=2).order_by('org__name'),
        'item_xlist': sro.orgsro_set.filter(publish=True, status=3).order_by('org__name')
    }

@login_required
@render_to('sro2/orglist/orglist_member.html')
def    orglist_publish_member(request, sro_id, item_id):
    '''
    @param sro_id:int - Sro.id (#FIXME: not need)
    @param item_id:int - OrgSro.id
    '''
    return upload_dict(OrgSro.objects.get(pk=item_id))

@login_required
def    orglist_publish_permit(request, sro_id, item_id):
    '''
    @param sro_id:int - Sro.id (#FIXME: not need)
    @param item_id:int - Permit.id
    render_to_response('sro2/stagelist/stagelist_html.html', RequestContext(request, {'stagelist': StageList.objects.get(pk=stagelist_id)}))
    '''
    return redirect('sro2.views.stagelist_html', stagelist_id=item_id)

def	__add_to_tar(tar, name, s):
	'''
	Add string 's' to tar 'tar' as file 'name' using tmp file 'tmp'
	'''
	tmp = tempfile.NamedTemporaryFile()	# for html-page
	tmp.write(s.encode('windows-1251'))
	tmp.flush()
	tar.add(tmp.name, name)
	tmp.close()

@login_required
def	orglist_upload(request, sro_id):
	'''FIXME'''
	sro = Sro.objects.get(pk=sro_id)
	item_list = sro.orgsro_set.filter(publish=True, status=2).order_by('org__name')
	item_xlist = sro.orgsro_set.filter(publish=True, status=3).order_by('org__name')
	# 1. Create files
	# 1.1. prepare
	tname = 'members.tar.gz'
	tarname = os.path.join(tempfile.gettempdir(), tname)
	tar = tarfile.open(tarname, mode="w:gz")
	# 1.2. main
	__add_to_tar(tar, 'members.html', loader.get_template('sro2/orglist/orglist_memberlist.html').render(Context({ 'sro': sro, 'item_list': item_list, 'item_xlist': item_xlist, })))
	# 1.3. each member
	for item in item_list | item_xlist:
		__add_to_tar(tar, 'member/%d.html' % item.id, loader.get_template('sro2/orglist/orglist_member.html').render(Context(upload_dict(item))))
		for perm in item.stagelist_set.all():
			if (perm.isperm()):
				__add_to_tar(tar, 'permit/%d.html' % perm.id, loader.get_template('sro2/stagelist/stagelist_html.html').render(Context({'stagelist': perm})))
	tar.close()
	# 2. upload via ftp
	hostname = sro.sroown.ftp
	hosts = netrc.netrc(os.path.join(STATIC_ROOT, 'sro2', 'netrc')).hosts
	if (not hosts.has_key(hostname)):
		return render_to_response('sro2/upload_msg.html', {'msg': "Check netrc"})
	login, acct, password = hosts[hostname]
	ftp = ftplib.FTP(host=hostname, user=login, passwd=password)
	ftp.storbinary('STOR %s' % os.path.join(sro.sroown.path, tname), open(tarname, "rb"))
	ftp.quit()
	os.remove(tarname)
	# 3. expand by ssh
	hostname = sro.sroown.sshhost
	hosts = netrc.netrc(os.path.join(STATIC_ROOT, 'sro2', 'netrc')).hosts
	if (not hosts.has_key(hostname)):
		return render_to_response('sro2/upload_msg.html', {'msg': "Check netrc"})
	login, acct, password = hosts[hostname]
	ssh = SSHClient()
	ssh.set_missing_host_key_policy(AutoAddPolicy())
	ssh.connect(hostname=hostname, username=login, password=password)
	response = ssh.exec_command('cd %s && rm -f members.html member/* permit/* && tar xfv %s' % (sro.sroown.path, tname))[1].read()
	ssh.close()
	# 4. that's all
	return render_to_response('sro2/upload_msg.html', RequestContext(request, {'msg': "Uploaded OK:", 'comments': response}))

@login_required
@render_to('sro2/orglist/orglist_table.html')
def    orglist_table(request, sro_id):
    sro = Sro.objects.get(pk=sro_id)
    orgsro_list = sro.orgsro_set.all().order_by('org__name')
    return {'orgsro_list': orgsro_list}

def    __multi(qset, sep=u'\n'):
    fields = list()
    for item in qset:
        fields.append(item.asstr())
    return sep.join(fields)

@login_required
def    orglist_csv(request, sro_id):
    '''
    Output SRO data as CSV for import from Excel.
    '''
    sro = Sro.objects.get(pk=sro_id)
    orgsro_list = sro.orgsro_set.all().order_by('org__name')
    statuses=[u'Нет',u'Кандидат',u'Член НП',u'Исключен','Архив']
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = '; filename=table.csv'
    e = csv.writer(response, dialect='excel', delimiter=';')
    # start
    e.writerow((
        u'№ п/п',
        u'Краткое наименование',
        u'Полное наименование',
        u'ОКОПФ',
        u'Дата в ЕГРЮЛ',
        u'ИНН',
        u'КПП',
        u'ОГРН (СГРП)',
        u'ОКАТО',
        u'Адрес юридический',
        u'Адрес фактический',
        u'Статус в СРО',
        u'Реестровый №',
        u'Дата членства в НП',
        u'Дата оплаты взноса в КФ',
        u'Сумма взноса в КФ',
        u'Дата оплаты ВВ',
        u'Публиковать',
        u'Номер лицензии на соответствующий вид работ',
        u'Стрх. страховщик',
        u'Стрх. Дог. #',
        u'Стрх. Статус',
        u'Стрх. Дог. от',
        u'Стрх. с',
        u'Стрх. по',
        u'Стрх. Сумма',
        u'Телефоны',
        u'Email',
        u'WWW',
        u'Руководство',
        u'Персонал',
        u'ОКВЭД',
        ))
    for i, orgsro in enumerate(orgsro_list):
        data = [
            i + 1,
            orgsro.org.name,
            orgsro.org.okopf.name + ' ' + orgsro.org.fullname,
            orgsro.org.okopf,
            orgsro.org.egruldate,
            orgsro.org.inn,
            orgsro.org.kpp,
            orgsro.org.ogrn,
            orgsro.org.okato,
            orgsro.org.laddress,
            orgsro.org.raddress,
            statuses[orgsro.status] or '',
            orgsro.regno or '',
            orgsro.regdate or '',
            orgsro.paydate or '',
            orgsro.paysum,
            orgsro.paydatevv,
            orgsro.publish,
        ]
        # License
        if (OrgLicense.objects.filter(orgsro=orgsro).count()): item = u'%s, с %s по %s' % (orgsro.orglicense.no, orgsro.orglicense.datefrom, orgsro.orglicense.datedue)
        else: item = ''
        data.append(item)
        # Insurance
        if (OrgInsurance.objects.filter(orgsro=orgsro).count()):
            inss=OrgInsurance.objects.filter(orgsro=orgsro)
            item = ['', '', '', '', '', '', '']
            for ins in inss:
                sts='Не действующая'
                if ins.active:
                    sts='Действующая'
                i = [
                    ins.insurer.name,
                    ins.no,
                    sts,
                    ins.date,
                    ins.datefrom,
                    ins.datedue,
                    ins.sum,
                ]
                n=0
                for cell in i:
                    item[n]+='\n'+str(cell)
                    n+=1
                #data.extend(item)
        else:
            item = ['', '', '', '', '', '','']
        data.extend(item)
        # Phone
        data.append(__multi(orgsro.org.contactphone_set.all()))
        # Email
        data.append(__multi(orgsro.org.contactemail_set.all()))
        # WWW
        data.append(__multi(orgsro.org.contactwww_set.all()))
        # Руководство
        data.append(__multi(orgsro.org.orgstuff_set.filter(leader=True)))
        # Персонал
        person_list=orgsro.org.orgstuff_set.all()
        pstr=''
        for p in person_list:
            workrange=''
            if p.startdate:
                workrange=' ( c %s ' % strdatedot(p.startdate)
                if not p.enddate:
                    workrange+=')'
                else:
                    workrange+=' по %s )' % strdatedot(p.enddate)
            elif p.enddate:
                workrange+=' ( по %s )' % strdatedot(p.enddate)
            pstr+='\n'+p.asstr()+workrange
        data.append(pstr)

        #data.append(__multi(orgsro.org.orgstuff_set.all()))
        # ОКВЭД
        data.append(__multi(orgsro.org.orgokved_set.all()))
        # write
        e.writerow(data)
    #response.write(loader.get_template('sro2/orglist/sro_table.csv').render(Context(RequestContext(request, {'orgsro_list': orgsro_list}))).encode('windows-1251'))
    # end
    return response

@login_required
def    orglist_rtn(request, sro_id, ulflag):
    ip = Okopf.objects.get(pk=91)
    sro = Sro.objects.get(pk=sro_id)
    if ulflag:
        orgsro_list = sro.orgsro_set.filter(publish=True).order_by('org__name')
        namehead = u'Наименование ЮЛ'
        filename = sro.sroown.tplprefix + '_ul.csv'
    else:
        orgsro_list = sro.orgsro_set.filter(publish=True).order_by('org__name')
        namehead = u'Наименование ИП'
        filename = sro.sroown.tplprefix + '_ip.csv'
    f = tempfile.NamedTemporaryFile()
    e = csv.writer(f, dialect='excel', delimiter='\t')
    # start
    e.writerow((
        u'№ п/п',
        u'Вид деятельности (ОКВЭД)',
        u'Перечень видов работ, оказывающих влияние на безопасность объектов капитального строительства',
        namehead,
        u'ИНН',
        u'ОГРН (СГРП)',
        u'Номер лицензии на соответствующий вид работ',
        u'Является ли член саморегулируемой организации аффилированным лицом по отношению к другим членам данного СРО',
        u'ОКАТО',
        u'Адрес юридический',
        u'Телефоны',
        u'WWW',
        u'Email',
        ))
    i = 1
    for orgsro in orgsro_list:
        if (orgsro.org.okopf == ip) is not ulflag:
            # License
            if (OrgLicense.objects.filter(orgsro=orgsro).count()): license = u'%s, с %s по %s' % (orgsro.orglicense.no, orgsro.orglicense.datefrom, orgsro.orglicense.datedue)
            else: license = ''
            # Виды работ
            if (ulflag):
                orgname = orgsro.org.okopf.name + ' ' + orgsro.org.fullname
            else:
                orgname = orgsro.org.fullname
            # All together
            data = [
                i,
                __multi(orgsro.org.orgokved_set.all()),
                orgsro.permits2str(u'\n'),
                orgname,
                orgsro.org.inn,
                orgsro.org.ogrn,
                license,
                'Нет',
                orgsro.org.okato,
                orgsro.org.laddress,
                __multi(orgsro.org.contactphone_set.all()),
                __multi(orgsro.org.contactwww_set.all()),
                __multi(orgsro.org.contactemail_set.all()),
            ]
            # write
            e.writerow(data)
            i += 1
    f.flush()
    f.seek(0)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = '; filename=' + filename
    response.write(f.read())
    f.close()
    #os.unlink(f.name)
    return response

@login_required
def    orglist_rtnu(request, sro_id):
    return orglist_rtn(request, sro_id, True)

@login_required
def    orglist_rtne(request, sro_id):
    return orglist_rtn(request, sro_id, False)

def    make_table(orgs,sro):
    '''
    Make orgs table for rtf doc (RTN report)

    * init pyrtf table
    * iterate orgs array
    * format tr
    * add row to table
    * return rtf table
    '''
    table = Table( TabPropertySet.DEFAULT_WIDTH, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 8 , TabPropertySet.DEFAULT_WIDTH * 4, TabPropertySet.DEFAULT_WIDTH * 4, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 4, TabPropertySet.DEFAULT_WIDTH * 4, TabPropertySet.DEFAULT_WIDTH * 7)
    #c1 = Cell( Paragraph( ' № п/п '   ) )
    row=[u'№ п/п',u'Вид деятельности ',u' Перечень видов работ, оказывающих влияние на безопасность объектов капитального строительства ',u' Организационно-правовая форма организации ',u' Полное наименование организации ',u' Идентификационный номер налогоплательщика (ИНН) ',u' Основной государственный регистрационный номер ',u' Номер лицензии на соответствующий вид работ ',u' Является ли член саморегулируемой организации аффилированным лицом по отношению к другим членам данного СРО ',u' Место нахождения, контактные данные (почтовый индекс, субъект Российской Федерации, район, город (населенный пункт), улица (проспект, переулок и др.) и номер дома (владения), корпуса (строения) и офиса, телефон, факс, адрес сайта в сети Интернет, электронная почта)']
    thin_edge  = BorderPropertySet( width=20, style=BorderPropertySet.SINGLE )
    thin_frame  = FramePropertySet( thin_edge,  thin_edge,  thin_edge,  thin_edge )

    n=0
    for cell in row:
        row[n]=Cell(Paragraph(row[n]),thin_frame)
        n+=1
    table.AddRow( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    row=range(1,11)
    n=0
    for cell in row:
        row[n]=Cell(Paragraph(str(row[n])),thin_frame)
        n+=1
    table.AddRow( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    num=1
    #TODO clean this. I dont know how.=(
    if sro.id == 1:
        deyat=u'Строительство, реконструкция, капитальный ремонт'
    if sro.id == 2:
        deyat=u'Подготовка проектной документации'
    for org in orgs:
        '''
        Fix this terrible code!
        '''
        try:
            license='%s от %s' % (org.orglicense.no,org.orglicense.datefrom.strftime("%d.%m.%Y") )
        except:
            license=''
        #try:
        hist=History(org)
        permits=hist.permits2str(u'\n')
        hist_str=''
        history=hist.history
        if history and org.status==2:
            hh=[]
            for h in history:
                hh.insert(0,h)
            history=hh
            for h in history:
                if h != history[0]:
                    hist_str+='%s\n' % h['desc'].replace('<b>','').replace('</b>','').replace('<br>','\n')
            if hist_str:
                hist_str='\n-----'+'\n'+hist_str
            permits='%s%s' % (permits,hist_str)
        prevs=hist.prevs()
        if prevs:
            permits += (u'\nРанее выданные:')
            for stagelist in prevs:
                permits += (u'\nСвидетельство № ' + stagelist.no + u' от ' + strdatedot(stagelist.date)+' ')
                if stagelist.protocol:
                    permits += stagelist.protocol.asstr_full()
        #except:
            #permits=''
        if org.id in [652,550,648,691]:
            permits='Реестровый номер %s, Свидетельства о допуске к работам не выдавалось.' % org.regno
        phones=''
        wwws=''
        mails=''
        for phone in org.org.contactphone_set.all():
            phones='%s, %s' % (phones,phone)
        if phones.startswith(','):
            phones=phones[2:]
        for www in org.org.contactwww_set.all():
            wwws='%s, %s' % (wwws,www)
        if wwws.startswith(','):
            wwws=wwws[2:]
        for mail in org.org.contactemail_set.all():
            mails='%s, %s' % (mails,mail)
        if mails.startswith(','):
            mails=mails[2:]
#!!!!!!!!!!!!!!!!!
        row=[str(num),deyat,permits,org.org.okopf.name,'%s %s' % (org.org.okopf.name,org.org.fullname),org.org.inn,org.org.ogrn,license,u'Нет','%s, %s, %s, %s' % (org.org.laddress,phones,wwws,mails)]
#!!!!!!!!!!!!!!!!!
        num+=1
        n=0
        for cell in row:
            if n!=2:
                row[n]=Cell(Paragraph(cell),thin_frame)
            elif permits:
                ps=permits.split('\n')
                pps=Cell()
                for p in ps:
                    pps.append(Paragraph(p))
                row[n]=pps
            else:
                row[n]=Cell(Paragraph(cell),thin_frame)
            n+=1
        table.AddRow( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    return table

@login_required
def    orglist_rtnh(request, sro_id):
    '''
    RTN report

    * init pyrtf doc
    * get orgs
    * make tables for orgs and ips
    * dump rtf doc
    '''
    doc, section, styles = RTFTestCase.initializeDoc()
    p = Paragraph( styles.ParagraphStyles.Heading1 )
    sro = Sro.objects.get(pk=sro_id)
    now=time.strftime("%d.%m.%Y %H:%M:%S")
    p.append( 'Реестр членов Некоммерческого партнерства саморегулируемой организации %s на %s' % (sro.fullname,now) )
    section.append( p )
    p = Paragraph( styles.ParagraphStyles.Heading2 )
    p.append(u'Юридичесчкие лица:')
    section.append( p )

    ip = Okopf.objects.get(pk=91)
    orgs=Sro.objects.get(pk=sro_id).orgsro_set.filter(~Q(org__okopf=ip)).exclude(status__lt=2).exclude(status=4).order_by('org__name')
    section.append( make_table(orgs,sro))

    orgs=Sro.objects.get(pk=sro_id).orgsro_set.filter(org__okopf=ip).exclude(status__lt=2).exclude(status=4).order_by('org__name')
    if orgs:
        p = Paragraph( styles.ParagraphStyles.Heading2 )
        p.append(u'ИП:')
        section.append( p )
        section.append( make_table(orgs,sro))
    sro_name=sro.sroown.tplprefix
    filename='RTN-%s(%s).rtf' % (sro_name,now.replace(' ','_'))
    path='%s/%s' % (MEDIA_ROOT,filename)
    doc.write(str(path))
    return HttpResponse(filename)

@login_required
@render_to('sro2/orglist/orglist_mailto.html')
def    orglist_mail_sel(request,orgs):
    '''
    Render emails list for selected orgs

    * dump json orgs array
    * gen email string
    '''
    s = sep = ""
    import simplejson
    orgs=simplejson.loads(orgs)
    id_list = orgs['orgs']
    org_list = Org.objects.filter(id__in=id_list).order_by('name')
    for org in org_list:
        for i in org.contactemail_set.all():
            s = s + sep + i.email.URL
            if not sep:
                sep = ", "
    return {'mailto': s}

@login_required
def    orglist_print_envelope(request, orgs):
    org_list, sro, name = orglist_print(request, orgs)
    template_name = os.path.join('sro2', 'orglist/orglist_print_envelope.rml')
    return pdf_render_to_response(template_name, {'org_list': org_list, 'user': request.user.username, 'name': name, 'sro': sro.name}, filename = 'envelopes_' + name + '.pdf')

@login_required
def    orglist_print_notification(request, orgs):
    org_list, sro, name = orglist_print(request, orgs)
    template_name = os.path.join('sro2', 'orglist/orglist_print_notification.rml')
    return pdf_render_to_response(template_name, {'org_list': org_list, 'user': request.user.username, 'name': name, 'sro': sro.name}, filename = 'notifications_' + name + '.pdf')

@login_required
def    orglist_print(request,orgs):
    import simplejson
    orgs=simplejson.loads(orgs)
    sro_id = orgs['sro_id']
    sro = Sro.objects.get(pk=sro_id)
    id_list = orgs['orgs']
    org_list = Org.objects.filter(id__in=id_list).order_by('name')
    name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return (org_list, sro, name)

@login_required
@render_to('sro2/orglist/orglist_print_maillist.html')
def    orglist_print_maillist(request, orgs):
    org_list, sro, name = orglist_print(request, orgs)
    return {
        'sro': sro,
        'org_list': org_list,
        'orgs': orgs
    }
    
@login_required
@render_to('sro2/orglist/orglist_org_add.html')
def    orglist_org_add(request, sro_id):
    sro = Sro.objects.get(pk=sro_id)
    org = Org()
    if request.method == 'POST':
        form = OrgAddForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save(commit=False)
            org.user=request.user
            org.save()
#            log_it(request, org, ADDITION)
            orgsro = OrgSro(org=org, sro=sro, user=request.user)
            orgsro.save()
#            log_it(request, orgsro, ADDITION)
            #return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
            return redirect('sro2.orgsro.views.orgsro_view',orgsro_id=orgsro.id)
    else:
        form = OrgAddForm(instance=org)
        okopf =  Okopf.objects.all()
    return {'sro': sro, 'org': org, 'form': form}

@login_required
def    orglist_org_add_exists(request, sro_id):
    if request.method == 'POST':
        sro=Sro.objects.get(pk=sro_id)
        form = OrgAddExistsForm(sro, request.POST)
        if form.is_valid():
            org = form.cleaned_data['org']
            orgsro = OrgSro(org=org, sro=sro, user=request.user)
            orgsro.save()
#            log_it(request, orgsro, ADDITION)
    #return HttpResponseRedirect(reverse('sro2.views.sro_list', kwargs={'sro_id': sro_id}))
    return redirect(orglist_list,sro_id=sro_id)

@login_required
def    orglist_find(request, sro_id):
    sro = Sro.objects.get(pk=sro_id)
    new_ver =  StageVer.objects.get(pk=2)
    old_ver =  StageVer.objects.get(pk=1)
    stage_list = sro.type.stage_set.filter(ver=new_ver).order_by('id')
    stage_list_old = sro.type.stage_set.filter(ver=old_ver).order_by('id')
    if request.method == 'POST':    # add
        stage_id = request.POST['select_stage']
        if (stage_id == ""):
            stage_id = request.POST['select_stage_old']
        if (stage_id != ""):
            stage = Stage.objects.get(pk=stage_id)
            orgsro_list = sro.orgsro_set.filter(currperm__isnull=False, currperm__permitstage__stage=stage, publish=True).distinct()
            return render_to_response('sro2/orglist/orglist_find.html', RequestContext(request, {'sro': sro, 'stage_list': stage_list, 'stage_list_old': stage_list_old, 'orgsro_list': orgsro_list, 'stage': stage}))
        else:
            return render_to_response('sro2/orglist/orglist_find.html', RequestContext(request, {'sro': sro, 'stage_list': stage_list, 'stage_list_old': stage_list_old}))
    else:
        return render_to_response('sro2/orglist/orglist_find.html', RequestContext(request, {'sro': sro, 'stage_list': stage_list, 'stage_list_old': stage_list_old}))

