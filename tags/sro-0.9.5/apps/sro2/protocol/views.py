# -*- coding: utf-8 -*-
'''
Protocol views
--------------
'''

from sro2.shared import *
import simplejson

@login_required
@render_to('sro2/protocol/protocol_list.html')
def    protocol_list(request, sro_id):
    '''
    List all protocols
    '''
    sro = Sro.objects.get(pk=sro_id)
    protocol_list = Protocol.objects.filter(sro=sro).order_by('date')
    return {'sro': sro, 'protocol_list': protocol_list}

@login_required
@render_to('sro2/protocol/protocol_view.html')
def    protocol_view(request, protocol_id):
    '''
    View protocol
    '''
    protocol = Protocol.objects.get(pk=protocol_id)
    return {'sro': Sro.objects.get(pk=protocol.sro.id), 'protocol' : protocol}

@login_required
@render_to('sro2/protocol/protocol_main.html')
def    protocol_main(request, protocol_id):
    '''
    im dont know why this method named like this...
    '''
    protocol = Protocol.objects.get(pk=protocol_id)
    sro_id = protocol.sro.id
    if request.method == 'POST':
        form = ProtocolMainForm(request.POST, instance=protocol)
        if form.is_valid():
            item = form.save()
            #log_it(request, item, ADDITION)
            return redirect(protocol_list,sro_id=sro_id)
    else:
        form = ProtocolMainForm(instance=protocol)
    return {'sro': Sro.objects.get(pk=sro_id), 'protocol': protocol, 'form': form}

@login_required
@render_to('sro2/protocol/protocol_main.html')
def    protocol_add(request, sro_id):
    '''
    Add new protocol
    '''
    sro = Sro.objects.get(pk=sro_id)
    protocol = Protocol()
    if request.method == 'POST':
        form = ProtocolMainForm(request.POST, instance=protocol)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.sro = sro
            new_item.save()
            #log_it(request, new_item, ADDITION)
            return redirect(protocol_list,sro_id=sro_id)
    else:
        protocol=False
        form = ProtocolMainForm()
    return {'sro': sro, 'protocol': protocol, 'form': form}

@login_required
def    protocol_del(request, protocol_id):
    '''
    Delete protocol
    '''
    protocol = Protocol.objects.get(pk=protocol_id)
    sro_id = protocol.sro.id
    # if there isn't any permit for deleting protocol
    if (protocol.permit_set.count() == 0):
        try:
            #log_it(request, protocol, DELETION)
            protocol.delete()
        except:
            pass
    #return HttpResponseRedirect(reverse('sro2.views.protocol_list', kwargs={'sro_id': sro_id}))
    return redirect(protocol_list,sro_id=sro_id)

@login_required
def    protocol_rtn(request, protocol_id):
    '''
    RTN report by this protocol

    # !!!NOT USED!!!

    * everything like sro_rtnh
    '''
    protocol_id=int(protocol_id)
    orgs=[]
    doc, section, styles = RTFTestCase.initializeDoc()
    p = Paragraph( styles.ParagraphStyles.Heading1 )
    sro = Sro.objects.get(pk=protocol.sro.id)
    now=time.strftime("%d.%m.%Y %H:%M:%S")
    protocol=Protocol.objects.get(pk=protocol_id)
    p.append( 'Сведения, вносимые в реестр членов Некоммерческого партнерства саморегулируемой организации %s на основании Протокола № %s от %s' % (sro.fullname,protocol_id,protocol.date) )
    section.append( p )
    p = Paragraph( styles.ParagraphStyles.Heading2 )
    p.append(u'Юридичесчкие лица:')
    section.append( p )

    ip = Okopf.objects.get(pk=91)
    #orgs=Sro.objects.get(pk=sro_id).orgsro_set.filter(Q(publish=True) & ~Q(org__okopf=ip)).order_by('org__name')
    permits=protocol.permit_set.all()
    for permit in permits:
        orgs.append(permit.orgsro)
    section.append( make_table(orgs,sro))
    orgs=Sro.objects.get(pk=sro.id).orgsro_set.filter(publish=True, org__okopf=ip).order_by('org__name')
    if orgs:
        p = Paragraph( styles.ParagraphStyles.Heading2 )
        p.append(u'ИП:')
        section.append( p )
        section.append( make_table(orgs,sro))
    sro_name=sro.sroown.tplprefix
    filename='protocol-%s-%s.rtf' % (sro_name,protocol_id)
    doc.write('%s/%s' % (MEDIA_ROOT,filename))
    return HttpResponse(filename)






#God knows, I do not want to do it
def protocol_report(request,protocol_id):
    global protocol
    protocol=Protocol.objects.get(pk=protocol_id)
    permits=protocol.permit_set.all()
    global files
    files=[]
    global extract
    extract=[]
    global questions
    questions=[]

    global z
    global k
    global summary
    global orgs
    toch=[]
    toac=[]
    toex=OrgSro.objects.filter(exprotocol=protocol)
    orgs={'tochange':toch,'toaccept':toac, 'toexclude':toex}
    for permit in permits:
        h=History(permit.orgsro)
        permit.orgsro.accept=True
        if h.originals().count()!=1:
            toch.append(permit.orgsro)
        else:
            toac.append(permit.orgsro)
    for statement in protocol.statement_set.all():
        statement.orgsro.accept=False
        if Statement.objects.filter(orgsro=statement.orgsro).count()!=1:
            toch.append(statement.orgsro)
        else:
            toac.append(statement.orgsro)
    if not request.method == 'POST':
        return render_to_response('sro2/protocol/protocol_gendoc.html', \
                                  RequestContext(request, \
                                {'sro': protocol.sro, 'protocol': protocol,'permits':permits,'orgs':orgs}))
    else:
        global section
        global styles
        summary=[]
        doc, section, styles = RTFTestCase.initializeDoc()
        sro = Sro.objects.get(pk=protocol.sro.id)
        now=time.strftime("%d.%m.%Y %H:%M:%S")
        h1(u'ПРОТОКОЛ')
        nt(u'от %s №%s' % (strdatedot(protocol.date),protocol.no),True)
        nt(u'заседания Правления %s' % sro.name,True)
        name=sro.name
        nt(u'Основание заседания Правления – инициатива Заместителя Председателя Правления {0}.'.format(name),True)
        nt(u'Место проведения заседания Правления – г. Санкт-Петербург, ул. Марата, д. 42',True)
        nt(u'Председательствующий на заседании Правления – Заместитель Председателя Правления {0} Силкин В.А.'.format(name),True)
        nt(u'Из 7 членов Правления на заседании Правления присутствуют:',True)
        nt(u'        1. Силкин В.А. – Заместитель председателя Правления {0};'.format(name),True)
        nt(u'        2. Чичин И.С. – член Правления {0};'.format(name),True)
        nt(u'        3. Белоусов Г.В. – член Правления {0};'.format(name),True)
        nt(u'        4. Сасалин В.А. – член Правления {0};'.format(name),True)
        nt(u'        5. Лукъянчиков В.Г. – член Правления {0};'.format(name),True)
        nt(u'        6. Литавор С.А. – член Правления {0};'.format(name),True)
        nt(u'На заседании Правления присутствовали без права голосования следующие лица:',True)
        nt(u'- Кулаков С.В. – Первый заместитель исполнительного директора {0};'.format(name),True)
        nt(u'- Зимина М.Н. – ответственный секретарь заседания Правления.',True)
        h2(u'Открытие заседания: ',False,True)
        nt(u'Слушали: Председательствующего, который сообщил, что из _ членов Правления в заседании принимают участие _ членов Правления. Заседание Правления правомочно. ',True)
        nt(u'Председательствующий объявил заседание Правления открытым.',True)

        h2(u'О повестке дня заседания Правления.',False,True)
        nt(u'Слушали Председательствующего, который предложил утвердить повестку дня заседания Правления. ',True)
        nt(u'Голосовали: «за» - единогласно.',True)
        nt(u'Решили: Утвердить повестку дня заседания Правления.',True)

        h2(u'Повестка дня заседания Правления:',False,True)
        i=1
        if orgs['tochange']:
            quest=u'%s. О рассмотрении заявлений о внесении изменений в свидетельство о допуске к определенному виду или видам работ, которые оказывают влияние на безопасность объектов капитального строительства, поступивших от членов %s:' % (i,sro.name)
            h2(quest)
            questions.append(quest)
            i+=1
            n=1
            for org in orgs['tochange']:
                nt(u'    %d. %s %s' % (n,org.org.okopf.shortname or '',org.org.fullname))
                n+=1
#
        if orgs['toaccept']:
            quest=u'%s. О принятии новых членов в %s и о выдаче Свидетельств о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, на основании заявлений, поступивших от организаций: ' % (i,sro.name)
            h2(quest)
            questions.append(quest)
            i+=1
            n=1
            for org in orgs['toaccept']:
                nt(u'    %d. %s %s' % (n,org.org.okopf.shortname or '',org.org.fullname))
                n+=1


        if orgs['toexclude']:
            quest=u'%s. О прекращении членства на основании заявления, поступившего от члена %s' % (i,sro.name)
            h2(quest)
            questions.append(quest)
            n=1
            for org in orgs['toexclude']:
                nt(u'    %d. %s %s' % (n,org.org.okopf.shortname or '',org.org.fullname))
                n+=1

        global num
        num=1
        h2(u'ПО ВОПРОСУ № %s ПОВЕСТКИ ДНЯ' % num)

        n=1
        for orgsro in orgs['tochange']:
            hist=History(orgsro)
            ops=hist.originals()
            permit=ops[len(ops)-2]
            nt(u'Слушали: ')
            z=u'- Зимину М.Н., которая доложила присутствующим о поступившем заявлении о внесении изменений в свидетельство №{1} от {2} о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, от члена {0} - {6} {3} ({4}) (ИНН {5}), а также о результатах проверки представленных документов на соответствие требований, стандартов и правил саморегулирования {0}.'.format(name,permit.no,strdatedot(permit.date),permit.orgsro.org.fullname,permit.orgsro.org.shortname,permit.orgsro.org.inn,permit.orgsro.org.okopf.name)
            nt(z)

            if not orgsro.accept:
                k=u'- Кулакова С.В., который рекомендовал, согласно результатам проведенной проверки представленных с заявлением документов, отказать данному юридическому лицу во внесении изменений в свидетельство о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, в связи с несоответствием  данного юридического лица требованиям {0} к выдаче свидетельств о допуске к указанным в заявлении работам.'.format(name)
            else:
                k=u'- Кулакова С.В., который предложил внести изменения в свидетельство о допуске к работам с выдачей нового Свидетельства о допуске к заявленным работам, которые оказывают влияние на безопасность объектов капитального строительства.'
            nt(k)
            nt(u'Голосовали: «за» - __ голоса, «против» - нет, «воздержался» - нет.')

            h2(u'%s.%d. Приняли решение: ' % (num,n))
            if not orgsro.accept:
                h2(u'Отказать во внесении изменений в свидетельство (№{1} от {2} года) о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, заявленным членом {0} - {6} {3} ({4}) (ИНН {5}).'.format(name,permit.no,strdatedot(permit.date),permit.orgsro.org.fullname,permit.orgsro.org.shortname,permit.orgsro.org.inn,permit.orgsro.org.okopf.name),orgsro,True,counter=u'%d.%d.' % (num,n))
                notify(orgsro,type=1,accept=False)
            else:

                h2(u'Внести изменения в свидетельство (№{1} от {2} года) о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, с выдачей нового свидетельства о допуске к работам, заявленным членом {0} - {6} {3} ({4}) (ИНН {5}).'.format(name,permit.no,strdatedot(permit.date),permit.orgsro.org.fullname,permit.orgsro.org.shortname,permit.orgsro.org.inn,permit.orgsro.org.okopf.name),orgsro,True,counter=u'%d.%d.' % (num,n))
                notify(orgsro,type=1,accept=True)
            n+=1
            make_extract(orgsro)

        num+=1
        if orgs['toaccept'] and orgs['tochange']:
            h2(u'ПО ВОПРОСУ № %s ПОВЕСТКИ ДНЯ' % num)

        n=1
        for orgsro in orgs['toaccept']:
            nt(u'Слушали:')
            z=u'-Зимину М.Н., которая доложила присутствующим о поступившем заявлении о приеме в члены саморегулируемой организации и выдаче свидетельства о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, от организации – {3} {0} ({1}) (ИНН {2}), а также о результатах рассмотрения представленных документов на соответствие требованиям стандартов и правил саморегулируемой организации.'.format(orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,orgsro.org.okopf.name)
            nt(z)
            if orgsro.accept:
                k=u'Кулакова С.В., который предложил принять организацию в члены с выдачей Свидетельства о членстве и Свидетельства о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, в соответствии с заявленным перечнем работ.'
            else:
                k=u'- Кулакова С.В., который рекомендует в связи с несоответствием данного юридического лица требованиям {0} к выдаче свидетельства о допуске к указанным в заявлении работам, а также не представлением заявителем в полном объеме документов, предусмотренных требованиями саморегулируемой организации, отказать данному юридическому лицу в приеме в члены {0} и выдаче свидетельства о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства {0}.'.format(name)
            nt(k)
            nt(u'Голосовали: «за» - __ голоса, «против» - нет, «воздержался» - нет.')

            h2(u'%d.%d. Приняли решение:' % (num,n))
            if orgsro.accept:
                h2(u'{6}.{5}.1. Принять в члены {0} - {4} {1} ({2}) за реестровым номером {3}, с выдачей Свидетельства о членстве в соответствии с Положением о членстве в {0};'.format(name,orgsro.org.fullname,orgsro.org.shortname,orgsro.regno,orgsro.org.okopf.name,n,num),orgsro,True)
                h2(u'{6}.{5}.2. Выдать Свидетельство о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, согласно заявленному перечню, члену {0} - {4} {1} ({2}) (ИНН {3}).'.format(name,orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,orgsro.org.okopf.name,n,num),orgsro,True)
                notify(orgsro,type=2,accept=True)
            else:
                h2(u'{6}.{5}.1. В соответствии с п.п. 1,2 ч. 5 ст. 55.6 Градостроительного кодекса РФ,отказать в приеме в члены {0}, а также в выдаче Свидетельства о членстве и в выдаче Свидетельства о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства {4} {1} ({2}) (ИНН {3}).'.format(name,orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,orgsro.org.okopf.name,n,num),orgsro,True)
                h2(u'{4}.{3}.2. Разъяснить {1} {2}, что отказ в приеме в члены {0} не является препятствием для повторного обращения в партнерство в целях принятия в члены саморегулируемой организации.'.format(name,orgsro.org.okopf.name,orgsro.org.fullname,n,num),orgsro,True)
                notify(orgsro,type=2,accept=False)
            n+=1
            make_extract(orgsro)

        num+=1
        if orgs['toaccept'] and orgs['tochange'] and orgs['toexclude']:
            h2(u'ПО ВОПРОСУ № %s ПОВЕСТКИ ДНЯ' % num)


        n=1
        for orgsro in orgs['toexclude']:
            nt(u'Слушали:')
            z=u'- Зимину М.Н., которая доложила присутствующим о поступившем заявлении о добровольном выходе из членов {0} Общества с ограниченной ответственностью {1} (ИНН {2} , реестровый номер {2}).'.format(name,orgsro.org.fullname,orgsro.org.inn,orgsro.regno)
            nt(z)
            k=u'- Кулакова С.В., который предложил на основании заявления {1} {2} о добровольном выходе из членов саморегулируемой организации, в соответствии с п.1 ч.1 ст. 55.7 Градостроительного кодекса РФ, прекратить членство в {0}; выданные {1} {2} Свидетельства о членстве и о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, аннулировать.'.format(name, orgsro.org.okopf.name,orgsro.org.fullname)
            nt(k)
            nt(u'Голосовали: «за» - __ голоса, «против» - нет, «воздержался» - нет.')

            nt(u'%s.%s. Приняли решение:' % (num,n))
            h2(u'{5}.{0}.1. На основании заявления о добровольном выходе из членов саморегулируемой организации, в соответствии с п.1 ч.1 ст. 55.7 Градостроительного кодекса РФ, прекратить членство в {1} Общества с ограниченной ответственностью {2} (ИНН {3}, реестровый номер {4}).'.format(n,name,orgsro.org.fullname,orgsro.org.inn,orgsro.regno,num),orgsro,True)
            h=History(orgsro)
            perm=h.originals().reverse()[0]
            h2(u'{7}.{0}.2. Аннулировать выданные {1} {2} Свидетельства о членстве (№ {3} от {4} года) и о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства (№{5} от {6} года).'.format(n,orgsro.org.okopf.name,orgsro.org.fullname,orgsro.regno,strdatedot(orgsro.regdate),perm.no,strdatedot(perm.date),num),orgsro,True)
            notify(orgsro,type=3,accept=False)
            n+=1
            make_extract(orgsro)
        nt('    ')
        nt('    ')

        nt(u'Заместитель Председателя Правления: ')
        nt(u'Силкин В.А.')
        nt(u'Протокол составил: _________ ')
        nt(u'Ответственный секретарь заседания Правления ')
        nt(u'Зимина М.Н')

        sro_name=sro.sroown.tplprefix
        filename='report-%s-%s.rtf' % (sro_name,protocol_id)
        path='%s/%s' % (MEDIA_ROOT,filename)
        doc.write(str(path))
        files.append(str(path))

        doc, section, styles = RTFTestCase.initializeDoc()
        h1(u'РЕШЕНИЕ')
        h1(u'ПРАВЛЕНИЯ %s' % sro.name)
        h1(u'___ от %s' % strdatedot(protocol.date))
        nt(u'Рассмотрев поступившие заявления членов {0} о внесении изменений в ранее выданные свидетельства \
о допуске к работам, которые оказывают влияния на безопасность объектов капитального строительства, \
а также заявления юридических лиц о вступлении в члены {0} и выдаче Свидетельств о допуске к работам, \
которые оказывают влияние на безопасность объектов капитального строительства,'.format(name))
        nt(u'Правление решило:')

        for line in summary:
            h2(line['text'])

        nt(u'Заместитель Председателя Правления: ')
        nt(u'Силкин В.А.')

        filename='summary-%s-%s.rtf' % (sro_name,protocol_id)
        path='%s/%s' % (MEDIA_ROOT,filename)
        doc.write(str(path))
        files.append(str(path))

        doc, section, styles = RTFTestCase.initializeDoc()
        h1(u'Уведомление ростехнадзора')
        nt(u'Руководителю Федеральной службы')
        nt(u'по экологическому, технологическому')
        nt(u'и атомному надзору')
        nt(u'Н.Г. Кутьину')
        nt(u'Некоммерческое партнерство саморегулируемая организация {0} \
(внесено в государственный реестр саморегулируемых организаций за регистрационным номером {1}) \
в соответствии с требованиями Градостроительного кодекса РФ уведомляет орган надзора за саморегулируемыми \
организациями о принятии следующих решений постоянно действующим коллегиальным органом управления \
НП СРО «{2}» (Протокол заседания Правления НП СРО «{2}» от {3} № {4}):'.format(sro.fullname,sro.regno\
                                            ,name,strdatedot(protocol.date),protocol.no))
        h2(u'1. Рассмотрев заявления о внесении изменений в свидетельство о допуске к определенному виду \
или видам работ, которые оказывают влияние на безопасность объектов капитального строительства, \
поступивших от членов {0}:'.format(name))
        for line in summary:
            if line['text'].startswith('1'):
                nt('    '+line['text'])

        h2(u'2. Принять в члены {0} с выдачей Свидетельства о членстве в {0} и \
Свидетельств о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, \
следующие организации:'.format(name))

        for line in summary:
            if line['text'].startswith('2'):
                nt('    '+line['text'])

        h2(u'3. '.format(name))

        for line in summary:
            if line['text'].startswith('3'):
                nt('    '+line['text'])


        h2(u'Приложение: ')
        nt(u'- решения Правления {0} № ___ от {1} на __ листах.'.format(name,strdatedot(protocol.date)))
        nt(u'Первый заместитель исполнительного директора {0}'.format(name))
        nt(u'С.В. Кулаков')

        filename='letter-%s-%s.rtf' % (sro_name,protocol_id)
        path='%s/%s' % (MEDIA_ROOT,filename)
        doc.write(str(path))
        files.append(str(path))

        arname='report-%s-%s.tar.gz' % (sro_name,protocol_id)
        arpath='%s/%s' % (MEDIA_ROOT,arname)
        import tarfile, os
        tar = tarfile.open(arpath, "w:gz")
        for name in files:
            tar.add(name)
            os.remove(name)
        tar.close()

        return HttpResponse(arname)

def nt(text,toextract=False):
    global styles
    global section
    p=Paragraph(styles.ParagraphStyles.Normal)
    p.append(text)
    section.append(p)
    global extract
    if toextract:
        extract.append(text)


def h1(text):
    global styles
    global section
    p=Paragraph(styles.ParagraphStyles.Heading1)
    p.append(text)
    section.append(p)

def h2(text,orgsro='',save=False,toextract=False,counter=''):
    global styles
    global section
    global summary
    p=Paragraph(styles.ParagraphStyles.Heading2)
    p.append(text)
    section.append(p)
    if save:
        if counter:
            text=counter+' '+text
        summary.append({'text':text,'org':orgsro})
    global extract
    if toextract:
        extract.append(text)

def nnt(text):
    global styles
    global nsection
    p=Paragraph(styles.ParagraphStyles.Normal)
    p.append(text)
    nsection.append(p)


def nh1(text):
    global styles
    global nsection
    p=Paragraph(styles.ParagraphStyles.Heading1)
    p.append(text)
    nsection.append(p)

def nh2(text):
    global styles
    global nsection
    p=Paragraph(styles.ParagraphStyles.Heading2)
    p.append(text)
    nsection.append(p)


def make_extract(orgsro):
    global protocol
    global extract
    global nsection
    global num
    global questions
    global orgs
    global summary
    doc, nsection, styles = RTFTestCase.initializeDoc()

    nh2(u'ВЫПИСКА')
    nh2(u'из ПРОТОКОЛА')

    for line in extract:
        nnt(line)

    nnt(questions[int(num)-1])

    names=['tochange','toaccept','toexclude']
    n=1
    for org in orgs[names[num-1]]:
        if orgsro==org:
            break
        else:
            n+=1
    nnt(u'      %d. %s %s' % (n,orgsro.org.okopf.shortname,orgsro.org.fullname))

    nh2(u'ПО ВОПРОСУ № %s ПОВЕСТКИ ДНЯ' % num)
    nnt(z)
    nnt(k)

    nh2(u'{0}.{1} Приняли решение:'.format(num,n))
    for line in summary:
        if line['org']==orgsro:
            nh2(line['text'])

    nnt(u'Протокол подписан {0} года председателем Правления Рыбкиным В.Г., секретарем заседания Правления Зиминой М.Н.'.format(strdatedot(protocol.date)))
    nnt(u'Настоящая Выписка из Протокола № {0} Заседания Правления Некоммерческого партнерства саморегулируемой организации {1} от {2} года ВЕРНА:'.format(protocol.no,orgsro.sro.fullname,strdatedot(protocol.date)))

    nnt(u'Первый заместитель исполнительного директора {0}'.format(orgsro.sro.name))
    nnt(u'С.В. Кулаков')
    nnt(u'%s' % strdatedot(protocol.date))
    nnt('   ')
    sro_name=orgsro.sro.sroown.tplprefix
    filename='extract-%s-%s-%s.rtf' % (sro_name,protocol.id,orgsro.id)
    path='%s/%s' % (MEDIA_ROOT,filename)
    doc.write(str(path))
    files.append(str(path))


def notify(orgsro,type,accept):
    global protocol
    global nsection
    global files
    sro_name=orgsro.sro.sroown.tplprefix
    doc, nsection, styles = RTFTestCase.initializeDoc()
    permit=orgsro.currperm
    name=orgsro.sro.name

    nnt(u'Руководителю')
    nnt(u'%s' % orgsro.org.okopf.name)
    nnt(u'%s' % orgsro.org.fullname)
    nnt(u'----------------')
    addr=orgsro.org.getaddress('Юридический')
    if addr:
        addr=addr.mkfullname(False, False)
    else:
        addr=orgsro.org.laddress
    nnt(u'%s' % addr)

    nh1(u'Уведомления о внесении изменений в свидетельство')
    if type==1 and accept:
        hist=History(orgsro)
        ops=hist.originals()
        permit=ops[len(ops)-2]
        nnt(u'Уведомляем Вас о том, что решением Правления {0} от {6} (Протокол № {1}) \
внесено изменение в Свидетельство о допуске к работам, которые оказывают влияние на безопасность \
объектов капитального строительства, № {2} от {3} года, выданное {4}\
({5}) (ИНН {6}), в соответствии с заявленным перечнем.'.format(name,protocol.no,permit.no,strdatedot(permit.date),orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,strdatedot(protocol.date)))
        nnt(u'{6} {4} ({5}) выдано Свидетельство о допуске к работам, \
которые оказывают влияние на безопасность объектов капитального строительства за № {2} от {3} \
'.format(name,protocol.no,permit.no,strdatedot(permit.date),orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,orgsro.org.okopf.name))
    elif type==1 and not accept:
        nnt(u'Уведомляем Вас о том, что решением Правления {0} от дата {1} (Протокол № {2}) отказано \
{3} ({4}) (ИНН {5}), \
во внесении изменений в Свидетельство о допуске к работам, которые оказывают влияние на безопасность \
объектов капитального строительства, № {6} от {7} года , в связи с несоответствием \
{3} ({4}) требованиям {0} к выдаче свидетельств \
о допуске к указанным в заявлении работам.'.format(name,protocol.no,strdatedot(protocol.date),\
                                        orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,\
                                        permit.no,strdatedot(permit.date)))
    elif type==2 and accept:
        nnt(u'Уведомляем Вас о том, что решением Правления {0} от {8} (Протокол № {9}) \
{1} ({2}) (ИНН {3}), \
принято в члены {0}, с выдачей Свидетельства о членстве \
за номером № {4} от {5} года и Свидетельства о допуске к работам, \
которые оказывают влияние на безопасность объектов капитального строительства \
за № {6} от {7} года, в соответствии \
с заявленным перечнем. '.format(name,orgsro.org.fullname,orgsro.org.shortname,orgsro.org.inn,\
                                        orgsro.regno,strdatedot(orgsro.regdate),\
                                        permit.no,strdatedot(permit.date),strdatedot(protocol.date),protocol.no))
    elif type==2 and not accept:
        nnt(u'Уведомляем Вас о том, что решением Правления {0} от {1} (Протокол № {2}) отказано {6} {3} ({4})\
(ИНН {5}) в приеме в члены {0} и в выдаче Свидетельства о допуске к работам, \
которые оказывают влияние на безопасность объектов капитального строительства, \
в связи с несоответствием требованиям {0} к выдаче свидетельства о допуске к указанным в заявлении работам, \
а также не представлением заявителем в полном объеме документов, предусмотренных требованиями\
саморегулируемой организации. Отказ в приеме в члены {0} не является препятствием для повторного обращения \
в партнерство в целях принятия в члены саморегулируемой организации.\
        '.format(name,strdatedot(protocol.date),protocol.no,orgsro.org.fullname,\
                                         orgsro.org.shortname,orgsro.org.inn,orgsro.org.okopf.name))
    else:
        nnt(u'Уведомляем Вас о том, что решением Правления от {1} года (Протокол № {2}) на основании заявления о добровольном выходе из членов саморегулируемой организации, в соответствии с п.1 ч.1 ст. 55.7 Градостроительного кодекса РФ, прекращено членство в {0} {3} {4} (ИНН {5}, реестровый номер {6}).'.format(name,strdatedot(protocol.date),protocol.no,orgsro.org.okopf.name,orgsro.org.fullname,orgsro.org.inn,orgsro.regno))
        nnt(u'Кроме того, доводим до сведения, что ранее выданные свидетельства о членстве и о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, аннулированы.')
        hist=History(orgsro)
        permit=hist.originals().reverse()[0]
        nnt(u'Свидетельства о членстве от {1} года за реестровым номером {2} и Свидетельство о допуске к работам, которые оказывают влияние на безопасность объектов капитального строительства, от {3} за номером {4} необходимо возвратить в {0} в течение 10 дней с момента принятия решения. '.format(name,strdatedot(orgsro.regdate),orgsro.regno,strdatedot(permit.date),permit.no))

    nh2(u'Приложение: ')
    nnt(u'Выписка из протокола заседания Правления {0} № {2} от {1} на __ листах.'.format(name,strdatedot(protocol.date),protocol.no))
    nnt(u'Первый заместитель исполнительного директора {0}'.format(name))
    nnt(u'С.В. Кулаков')

    filename='notification-%s-%s-%s.rtf' % (sro_name,protocol.id,orgsro.id)
    path='%s/%s' % (MEDIA_ROOT,filename)
    doc.write(str(path))
    files.append(str(path))