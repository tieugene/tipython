# -*- coding: utf-8 -*-

from sro2.models import checkuser, Stage, Statement
from django import template
from sro2.views import strdatedot
from django.db.models import Max
#from sro2.shared import *

register = template.Library()

@register.filter
def	chkuser(obj, user):
	return checkuser(obj, user)

@register.filter
def	dquot(s):
	'''
	Return string w/ each quote doubled
	'''
	return s.replace('"', '""')

@register.filter_function
def	order_by(queryset, args):
	args = [x.strip() for x in args.split(',')]
	return queryset.order_by(*args)

@register.filter
def getstatus(status,classes=''):
	try:
		sts=['Нет','Кандидат','Член НП','Исключен','Архив']
		cls=['snone','scandidate','smember','sexclude','sarchive']
		if classes!='none':
			return '<div class="%s %s" id="status">%s</div>' % (classes,cls[status],sts[status])
		else:
			return sts[status]
	except:
		return 'Ошибка!'


@register.filter
def getsubstages(stage):
	try:
		substages = Stage.objects.filter(parent=stage).order_by('id')
		return substages
	except:
		return False

@register.filter
def getchecked(stage, string):	
	try:
		statement_id, danger = string.split(",")
		statement_id = int(statement_id)
		danger = int(danger)

		statement = Statement.objects.get(pk=statement_id)
		permitstage_list = statement.permitstage_set.filter(danger=danger, stage__parent=stage)
		if danger == 1:
			stage_list = Stage.objects.filter(parent=stage)
		else:
			stage_list = Stage.objects.filter(parent=stage, dangeronly=False)
		if permitstage_list.count() == stage_list.count():
			return True
		else:
			return False
	except:
		return False

@register.filter
def getlastcoursedate(courses):
	#try:
		return strdatedot(courses.aggregate(Max('coursedate'))['coursedate__max'])
	#except:
		return False


@register.filter
def getaddresstypes(contactaddr):

    types = ''
    for contact2addrtype in contactaddr.contact2addrtype_set.all():
        if types != '':
            types += ', '
            types += contact2addrtype.type.asstr().lower()        
        else:
            types += contact2addrtype.type.asstr().lower()
    return types

@register.filter
def getaddress(contact, type):

	return contact.getaddress(type)

@register.filter
def getaddress_fullname(contact, type):

	if contact.getaddress(type) == '':
		# to delete in future releases {
		try:
			if type == 'Почтовый' or type == 'Фактический':
				return contact.raddress[7:]
			else:
				return contact.laddress[7:]
		except:
		# } to delete in future releases
			return ''
	else:
		return contact.getaddress(type).mkfullname(False, False)


@register.filter
def getaddress_zip(contact, type):

	if contact.getaddress(type) == '':
		# to delete in future releases {
		try:
			if type == 'Почтовый' or type == 'Фактический':
				return contact.raddress[0:6]
			else:
				return contact.laddress[0:6]
		except:
		# } to delete in future releases
			return ''
	else:
		return str(contact.getaddress(type).zip)

'''
    to delete in jinja
'''
@register.filter
def get_case(wordcombination, case):

    return wordcombination.get_case()[case]

'''
    to delete in jinja
'''
@register.filter
def get_shortcase(wordcombination, case):

    return wordcombination.get_shortcase()[case]