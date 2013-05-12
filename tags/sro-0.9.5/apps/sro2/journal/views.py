# -*- coding: utf-8 -*-
'''
Journal views
-------------
'''
from sro2.shared import *
from datetime import datetime, date, time, timedelta
from django.contrib.contenttypes.models import ContentType

def process_logs(logs):
    processed_logs=[]
    for log in logs:
        try:
            ctype = ContentType.objects.get(pk=log.content_type_id)
            if ctype.id >= 9: # Contenttype не служебный, т.е. не группа, не пользователь и т.д.
                log.ctype = ctype.name
                model = ctype.model_class()
                obj = model.objects.get(pk=log.object_id)
                log.object = obj
        except:
            pass
        if hasattr(log,'object') or log.action_flag==3:
            processed_logs.append(log)

    return processed_logs

@render_to('sro2/journal/journal.html')
@superuser_only
def journal_ng(request,start_date='',end_date=''):

    if start_date and end_date:
        #если даты переданы, то созадаем из них объекты datetime
        day,mounth,year = start_date.split('.')
        eday,emounth,eyear = end_date.split('.')
        sd=date(int(year), int(mounth), int(day))
        ed=date(int(eyear), int(emounth), int(eday)+1)
    else:
        #а не переданы, делаем период, охватывающий последние сутки
        ed=datetime.today()
        sd=ed-timedelta(days=1)
    #делаем запрос, ограничивая датами.
    logs = LogEntry.objects.filter(action_time__gte=sd).filter(action_time__lte=ed)

    logs=process_logs(logs)
    return {
        'logs':logs
    }


@render_to('sro2/journal/journal.html')
@superuser_only
def journal_ng_obj(request,ctype,obj_id):

    links={
        OrgSro:[
                'org',
                'currperm',
                'obj.org.orgstuff_set.all()',
                'obj.stagelist_set.instance_of(Permit).all()',
                'obj.stagelist_set.instance_of(Statement).all()',
                'obj.orginsurance_set.all()',
                'OrgLicense.objects.filter(orgsro=obj)',
                'Phone.objects.filter(id__in=obj.org.contactphone_set.all().values_list("phone__id"))',
                'WWW.objects.filter(id__in=obj.org.contactwww_set.all().values_list("www__id"))',
                'Email.objects.filter(id__in=obj.org.contactemail_set.all().values_list("email__id"))',
        ],
        Person:[
                'obj.orgstuff_set.all()',
                'obj.personskill_set.all()'
        ],
        Permit:[
                'Permit.objects.filter(no=obj.no,status__gt=0)'
        ]
    }

    ctype=ContentType.objects.get(model=ctype)
    obj=ctype.model_class().objects.get(pk=obj_id)
    logs = LogEntry.objects.filter(content_type=ctype,object_id=obj_id)
    t=[]
    for log in logs:
        t.append(log)
    logs=t[:]
    if ctype.model_class() in links and links[ctype.model_class()]:
        for subobj_str in links[ctype.model_class()]:
            sublogs = []
            try:
                subobj=getattr(obj,subobj_str)
                sublogs = LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(subobj.__class__),object_id=subobj.id)
            except:
                eval_string=subobj_str
                try:
                    subset=eval(eval_string)
                    if subset.count():
                        ctype=ContentType.objects.get_for_model(subset[0].__class__)
                        for item in subset:
                            subsublogs = LogEntry.objects.filter(content_type=ctype,object_id=item.id)
                            for log in subsublogs:
                                sublogs.append(log)
                except:
                    pass
            if sublogs != []:
                t=[]
                for log in sublogs:
                    t.append(log)
                logs.extend(t)

    logs=sorted(process_logs(logs),key=gt,reverse=True)
    return {
        'logs':logs,
        'object':obj
    }

def gt(log): return log.action_time

@superuser_only
@render_to('sro2/journal.html')
def	journal(request,start_date='',end_date=''):
    '''
    Journal page to view system log (LogEntry)
    '''
    if start_date and end_date:
        #если даты переданы, то созадаем из них объекты datetime
        day,mounth,year = start_date.split('.')
        eday,emounth,eyear = end_date.split('.')
        sd=date(int(year), int(mounth), int(day))
        ed=date(int(eyear), int(emounth), int(eday)+1)
    else:
        #а не переданы, делаем период, охватывающий последние сутки
        ed=datetime.today()
        sd=ed-timedelta(days=1)
    #делаем запрос, ограничивая датами.
    log = LogEntry.objects.filter(action_time__gte=sd).filter(action_time__lte=ed)
    return { 'log':log,'sd':start_date,'ed':end_date }
