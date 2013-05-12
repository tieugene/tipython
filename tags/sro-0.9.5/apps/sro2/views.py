# -*- coding: utf-8 -*-
'''
SRO2 views
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
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext
from datetime import datetime, date as dt, date
import time
import sys
from models import *
###(1
from gw.models import *
###1)

reload(sys)
sys.setdefaultencoding("utf-8")

def	my_context(context):
    '''
    our context processor. Add to dict vars to send in ALL templates.
    '''
    sros=SroOwn.objects.all()
    return {
        'VERSION' : VERSION,
        'sros':sros,
    }

@login_required
def    unilist(request,obj,critline):
    '''
    Dirty hack
    '''
    cs=critline.split(',')
    info=[]
    for q in cs:
        i={}
        i['chain'], i['val'] = q.split('=')
        i['links']=i['chain'].split('__')
        info.append(i)

    result=eval('%s.objects.filter(%s)'%(obj,critline))
    for r in result:
        r.dict=r.__dict__
    return render_to_response('sro2/unilist.html',RequestContext(request, {'result':result,'obj':obj,'critline':critline,'info':info}))



def benchmark(request):
    report=[]
    startpoint=datetime.now()
    report.append('Start benchmark: %s' % startpoint)

    report.append('<h4>Test 1: QuerySet manipulation without "select_related"</h4>')
    list=OrgSro.objects.filter(sro__id=1)
    report.append('QuerySet items: <b>%s</b>' % list.count())
    for orgsro in list:
        temp=orgsro.org.fullname
        orgsro.temp='tttt'
    midpoint=datetime.now()
    report.append('QuerySet manipulate finished: %s' % midpoint)
    report.append('QuerySet manipulate actions:')
    report.append('Get orgsro.org.fullname')
    report.append('Do orgsro.temp="tttt"')
    d=midpoint-startpoint
    report.append('QuerySet manipulate time: <b>%s</b>' % d)


    report.append('<h4>Test 2: QuerySet manipulation with "select_related"</h4>')
    list=OrgSro.objects.filter(sro__id=1).select_related('org')
    report.append('QuerySet items: <b>%s</b>' % list.count())
    for orgsro in list:
        temp=orgsro.org.fullname
        orgsro.temp='tttt'
    midpoint2=datetime.now()
    report.append('QuerySet manipulate finished: %s' % midpoint)
    report.append('QuerySet manipulate actions:')
    report.append('Get orgsro.org.fullname')
    report.append('Do orgsro.temp="tttt"')
    d=midpoint2-midpoint
    report.append('QuerySet manipulate time: <b>%s</b>' % d)

    report.append('<h4>Test 3: OrgSro list render by <b>Django</b></h4>')
    html=render_to_response('sro2/orglist/orgtable.html',RequestContext(request, {'sro': Sro.objects.get(pk=1),'list': list,}))
    endpoint=datetime.now()
    report.append('OrgSro list rendered: %s' % endpoint)
    report.append('OrgSro list template: %s' % 'sro2/orglist/orgtable.html')
    d=endpoint-midpoint
    report.append('OrgSro list render time: <b>%s</b>' % d)

    report.append('<h4>Test 4: OrgSro list render by <b>Jinja2</b></h4>')
    from jinja2 import Environment,FileSystemLoader
    from settings import TEMPLATE_DIRS
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIRS[0]),autoescape=False)

    template = env.get_template('sro2/orglist/orgtable2.html')
    html=template.render({'sro': Sro.objects.get(pk=1),'list': list,})
    jinjapoint=datetime.now()

    report.append('OrgSro list rendered: %s' % endpoint)
    report.append('OrgSro list template: %s' % 'sro2/orglist/orgtable2.html')
    d=jinjapoint-endpoint
    report.append('OrgSro list render time: <b>%s</b>' % d)

    return HttpResponse('<br>'.join(report))



'''
def migrate_course(request):
    skills=PersonSkill.objects.filter(coursedate__isnull=False)
    sk=skills.count()
    for skill in skills:
        Course(personskill=skill,coursename=skill.coursename,courseno=skill.courseno,coursedate=skill.coursedate,courseschool=skill.courseschool).save()
        skill.coursename=None
        skill.courseno=None
        skill.coursedate=None
        skill.courseschool=None
        skill.save()
    return HttpResponse('Done, migrate %s courses' % sk)


def migrate_course_year(request):
    skills=PersonSkill.objects.filter(year__gt=0)
    sk=skills.count()
    for skill in skills:
        try:
            skill.skilldate=dt(int(skill.year),1,1)
        except Exception, e:
            #return HttpResponse(e)
            pass
        skill.year=0
        skill.save()
    return HttpResponse('Done, migrate %s years' % sk)

def clear_persons(request):
    ps=Person.objects.all()
    n=0
    for p in ps:
        if not p.orgstuff_set.count():
            p.delete()
            n+=1
    return HttpResponse('Done, delete %s persons' % n)

def models2gw(request):

    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute("""
        delete from `gw_okato` where 1;
        delete from `gw_okopf` where 1;
        delete from `gw_okved` where 1;
        delete from `gw_skill` where 1;
        delete from `gw_role` where 1;
        delete from `gw_speciality` where 1;

        insert into `gw_okato` select * from `sro2_okato`;
        insert into `gw_okopf` select * from `sro2_okopf`;
        insert into `gw_okved` select * from `sro2_okved`;
        insert into `gw_skill` select * from `sro2_skill`;
        insert into `gw_role` select * from `sro2_role`;
        insert into `gw_speciality` select * from `sro2_speciality`;

        delete from `gw_org` where 1;
        delete from `gw_orgokved` where 1;
        delete from `gw_www` where 1;
        delete from `gw_contactwww` where 1;
        delete from `gw_email` where 1;
        delete from `gw_contactemail` where 1;
        delete from `gw_phone` where 1;
        delete from `gw_contactphone` where 1;
        delete from `gw_phonetype` where 1;
        delete from `gw_phone2type` where 1;

        delete from `gw_person` where 1;
        delete from `gw_personskill` where 1;
        delete from `gw_course` where 1;
        delete from `gw_orgstuff` where 1;

        ALTER TABLE `gw_person` ADD COLUMN `user_id` INTEGER  DEFAULT NULL;
        ALTER TABLE `gw_org` ADD COLUMN `user_id` INTEGER  DEFAULT NULL;
    """)
    transaction.commit_unless_managed()

    from gw.contact.models import Org as Org2
    from gw.contact.models import Okopf as Okopf2
    from gw.contact.models import Okato as Okato2
    from gw.contact.models import Okved as Okved2
    from gw.contact.models import OrgOkved as OrgOkved2
    from gw.contact.models import ContactWWW as ContactWWW2
    from gw.bits.models import WWW as Www2
    from gw.contact.models import ContactEmail as ContactEmail2
    from gw.bits.models import Email as Email2
    from gw.contact.models import ContactPhone as ContactPhone2
    from gw.bits.models import Phone as Phone2
    from gw.bits.models import Phone2Type as Phone2Type2
    from gw.bits.models import PhoneType as PhoneType2
    from gw.contact.models import Person as Person2
    from gw.contact.models import PersonSkill as PersonSkill2
    from gw.contact.models import Course as Course2
    from gw.contact.models import Role as Role2
    from gw.contact.models import Speciality as Speciality2
    from gw.contact.models import Skill as Skill2
    from gw.bits.models import Phone as Phone2
    from gw.contact.models import OrgStuff as OrgStuff2

    fax = PhoneType2()
    fax.id = 0
    fax.abbr = "Факс"
    fax.name = "Факс"
    fax.save()

    for org in Org.objects.all():
        org2 = Org2()
        org2.name = org.name
        org2.shortname  = org.shortname
        org2.fullname   = org.fullname
        if org.okopf is not None:
            org2.okopf      = Okopf2.objects.get(pk=org.okopf.id)
        org2.egruldate  = org.egruldate
        org2.inn        = org.inn
        org2.kpp        = org.kpp
        org2.foreign    = org.foreign
        org2.ogrn       = org.ogrn
        if org.okato is not None:
            org2.okato      = Okato2.objects.get(id=org.okato.id)
        org2.laddress   = org.laddress
        org2.raddress   = org.raddress
        org2.comments   = org.comments
        if org.user is not None:
            org2.old_user_id = org.user.id
        org2.save()

        for orgokved in OrgOkved.objects.filter(org=org):
            orgokved2 = OrgOkved2()
            orgokved2.org = org2
            orgokved2.okved = Okved2.objects.get(pk=orgokved.okved.id)
            orgokved2.save()

        for orgwww in OrgWWW.objects.filter(org=org):

            if Www2.objects.filter(URL=orgwww.URL).count() > 0:
                contactwww2 = ContactWWW2()
                contactwww2.contact = org2
                contactwww2.www = Www2.objects.get(URL=orgwww.URL)
                contactwww2.save()
            else:
                www2 = Www2()
                www2.URL = orgwww.URL
                www2.save()

                contactwww2 = ContactWWW2()
                contactwww2.contact = org2
                contactwww2.www = www2
                contactwww2.save()

        for orgemail in OrgEmail.objects.filter(org=org):

            if Email2.objects.filter(URL=orgemail.URL).count() > 0:
                contactemail2 = ContactEmail2()
                contactemail2.contact = org2
                contactemail2.email = Email2.objects.get(URL=orgemail.URL)
                contactemail2.save()
            else:
                email2 = Email2()
                email2.URL = orgemail.URL
                email2.save()

                contactemail2 = ContactEmail2()
                contactemail2.contact = org2
                contactemail2.email = email2
                contactemail2.save()

        for orgphone in OrgPhone.objects.filter(org=org):

            newphone = orgphone.phone.replace(' ', '')[0:14]
            if Phone2.objects.filter(no=newphone).count() > 0:
                newphone2 = Phone2.objects.get(no=newphone)
                if ContactPhone2.objects.filter(contact=org2,phone=newphone2).count() == 0:
                    contactphone2 = ContactPhone2()
                    contactphone2.contact = org2
                    contactphone2.phone = newphone2
                    contactphone2.save()
            else:
                phone2 = Phone2()
                phone2.no = orgphone.phone.replace(' ', '')[0:14]
                phone2.save()

                contactphone2 = ContactPhone2()
                contactphone2.contact = org2
                contactphone2.phone = phone2
                contactphone2.save()

                if orgphone.phone.find('ф') != -1:
                    phone2type2 = Phone2Type2()
                    phone2type2.phone = phone2
                    phone2type2.type = fax
                    phone2type2.save()

        cursor2 = connection.cursor()
        cursor2.execute("""
            UPDATE sro2_orgsro SET org_id = %s WHERE org_id = %s;
            UPDATE sro2_personorgsro SET org_id = %s WHERE org_id = %s;
        """, [org2.id, org.id, org2.id, org.id])
        transaction.commit_unless_managed()

    for person in Person.objects.all():

        person2 = Person2()
        person2.firstname   = person.firstname
        person2.midname     = person.midname
        person2.lastname    = person.lastname
        if person.user is not None:
            person2.old_user_id = person.user.id
        person2.save()

        if person.phone is not None and person.phone != "":
            newphone = person.phone.replace(' ', '')[0:14]
            if Phone2.objects.filter(no=newphone).count() > 0:
                contactphone2 = ContactPhone2()
                contactphone2.contact = person2
                contactphone2.phone = Phone2.objects.get(no=newphone)
                contactphone2.save()
            else:
                phone2 = Phone2()
                phone2.no = newphone
                phone2.save()

                contactphone2 = ContactPhone2()
                contactphone2.contact = person2
                contactphone2.phone = phone2
                contactphone2.save()

        for personskill in person.personskill_set.all():
            personskill2 = PersonSkill2()
            personskill2.person = person2
            personskill2.speciality = Speciality2.objects.get(pk=personskill.speciality.id)
            personskill2.skill = Skill2.objects.get(pk=personskill.skill.id)
            personskill2.year = personskill.year
            personskill2.skilldate = personskill.skilldate
            personskill2.school = personskill.school
            personskill2.seniority = personskill.seniority
            personskill2.seniodate = personskill.seniodate
            personskill2.tested = personskill.tested
            personskill2.save()

            for course in Course.objects.filter(personskill=personskill):
                course2 = Course2()
                course2.personskill = personskill2 
                course2.courseno =  course.courseno
                course2.coursedate = course.coursedate
                course2.coursename = course.coursename
                course2.courseschool = course.courseschool
                course2.save()

        for orgstuff in OrgStuff.objects.filter(person=person):
            orgstuff2 = OrgStuff2()
            orgstuff2.org = Org2.objects.get(inn=orgstuff.org.inn)
            orgstuff2.role = Role2.objects.get(pk=orgstuff.role.id)
            orgstuff2.person = person2
            orgstuff2.leader = orgstuff.leader
            orgstuff2.permanent = orgstuff.permanent
            orgstuff2.startdate = orgstuff.startdate
            orgstuff2.enddate = orgstuff.enddate
            orgstuff2.save()

        cursor3 = connection.cursor()2gw(request):

    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute("""
        delete from `gw_okato` where 1;
        delete from `gw_okopf` where 1;
        delete from `gw_okved` where 1;
        delete from `gw_skill` where 1;
        delete from `gw_role` where 1;
        delete from `gw_speciality` where 1;

        insert into `gw_okato` select * from `sro2_okato`;
        insert into `gw_o
        cursor3.execute("""
            UPDATE sro2_personorgsro SET person_id = %s WHERE person_id = %s;
        """, [person2.id, person.id])
        transaction.commit_unless_managed()

    cursor1 = connection.cursor()
    cursor1.execute("""
        UPDATE gw_person SET user_id = old_user_id;
        UPDATE gw_org SET user_id = old_user_id;
    """)
    transaction.commit_unless_managed()

    return HttpResponse('XXX')
'''

from sro2.jnj import *
from sro2.stagelist.views import *
from sro2.statement.views import *
from sro2.permit.views import *
from sro2.alienpermit.views import *
from sro2.person.views import *
from sro2.protocol.views import *
from sro2.orglist.views import *
from sro2.report.views import *
from sro2.orgsro.views import *
from sro2.sro.views import *
from sro2.journal.views import *

@login_required
@render_to('sro2/about.html')
def about(request):
    return {}