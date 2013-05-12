# -*- coding: utf-8 -*-
'''
'''
from django.http import HttpResponse
import sys
from sro2.models import *

reload(sys)
sys.setdefaultencoding("utf-8")

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
        if org.okopf != None:
            org2.okopf      = Okopf2.objects.get(pk=org.okopf.id)
        org2.egruldate  = org.egruldate
        org2.inn        = org.inn
        org2.kpp        = org.kpp
        org2.foreign    = org.foreign
        org2.ogrn       = org.ogrn
        if org.okato != None:
            org2.okato      = Okato2.objects.get(id=org.okato.id)
        org2.laddress   = org.laddress
        org2.raddress   = org.raddress
        org2.comments   = org.comments
        if org.user != None:
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
        if person.user != None:
            person2.old_user_id = person.user.id
        person2.save()

        if person.phone != None and person.phone != "":
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

        cursor3 = connection.cursor()
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
