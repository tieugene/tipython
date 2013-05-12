# -*- coding: utf-8 -*-

'''
It seems that _nested_ formsets are too hard to aprove.
So - solution is:
	* just 1 level of formsets
	* form - separately, formset[s] - separately
'''

__legend = '''\
<p> Согласно Приказу ФНС от 25.01.12 N ММВ-7-6/25@. </p>\
<p> Для регистрации ИП необходимо таже заполнить ПД-4сб (пример есть на странице этой квитанции) и - если предполагается УСН - Заявление на УСН. </p>\
'''

# 1. django
from django import forms
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.forms.extras.widgets import SelectDateWidget

# 2. 3rd party

# 3. system
import sys, pprint, datetime

# 4. my
import utils
from consts import *
from dox.models import SSRF, Okved

reload(sys)
sys.setdefaultencoding('utf-8')

list_sex = [
	(1, 'мужской'),
	(2, 'женский'),
]
list_citizenship = [
	(1, 'РФ'),
	(2, 'Иностранец'),
	(3, 'Бомж'),
]

list_adult = [
	(1, 'Опекуны согласны'),
	(2, 'Брак'),
	(3, 'Суд объявил дееспособным'),
	(4, 'Орган опеки объявил дееспособным'),
]

list_perm = [
	(1, 'ВНЖ'),
	(2, 'РВП'),
]

DATA = {
	K_T_UUID:	'C9B0FA3ACED04F5E88131626A3881BBF',
	K_T_NAME:	'Форма 21001',
	K_T_COMMENTS:	'Заявление о государственной регистрации физического лица в качестве индивидуального предпринимателя',
	K_T_LEGEND:	__legend,
	K_T_FIELD:	SortedDict([
		('spro_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Регистрирующая организация',
					'help_text':	'в винительном падеже',
				}
		}),
		('spro_id', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'Код СПРО',
				}
		}),
		('lastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Фамилия',
				}
		}),
		('firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имя',
				}
		}),
		('midname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Отчество',
					'required':	False,
				}
		}),
		('sex', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Пол',
					'help_text':	'по паспорту',
				}
		}),
		('birthdate', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата рождения',
				}
		}),
		('birthplace', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место рождения',
				}
		}),
		('citizenship', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Гражданство',
					'choices':	list_citizenship,
				}
		}),
		('country', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Страна гражданства',
					'required':	False,
				}
		}),
		('elastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Фамилия',
					'required':	False,
				}
		}),
		('efirstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имя',
					'required':	False,
				}
		}),
		('emidname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Отчество',
					'required':	False,
				}
		}),
		('inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'min_length':	12,
					'required':	False,
				}
		}),
		('addr_zip', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Индекс',
				}
		}),
		('addr_srf', {
				K_T_FIELD_T:	K_MODEL_FIELD,
				K_T_FIELD_A:	{
					'label':	'Субъект РФ',
					'queryset':	SSRF.objects.all(),
					'empty_label':	None,
				}
		}),
		('addr_region', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Район',
					'required':	False,
				}
		}),
		('addr_city', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Город',
					'required':	False,
				}
		}),
		('addr_locality', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Населенный пункт',
					'required':	False,
				}
		}),
		('addr_street', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'улица',
					'help_text':	'проспект, переулок и т.д.',
				}
		}),
		('addr_house', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дом',
					'help_text':	'Полностью. Пример: дом 3',
				}
		}),
		('addr_building', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Строение',
					'help_text':	'корпус, литер - полностью',
					'required':	False,
				}
		}),
		('addr_app', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'квартира',
					'help_text':	'офис, помещение - полностью',
					'required':	False,
				}
		}),
		('phone_code', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Код',
					'required':	False,
				}
		}),
		('phone_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'required':	False,
				}
		}),
		('phone_fax', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Факс',
					'required':	False,
				}
		}),
		('doc_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Тип',
				}
		}),
		('doc_series', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Серия',
					'min_length':	4,
					'max_length':	4,
					'required':	False,
				}
		}),
		('doc_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'min_length':	6,
				}
		}),
		('doc_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Когда выдан',
				}
		}),
		('doc_whom', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кем выдан',
				}
		}),
		('doc_kp', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Код подразделения',
					'min_length':	6,
					'max_length':	6,
					'required':	False,
				}
		}),
		('adult', {
				K_T_FIELD_T:	K_BOOL_FIELD,
				K_T_FIELD_A:	{
					'label':	'Совершеннолетний',
					'required':	False,
				}
		}),
		('adult_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Основание',
					'choices':	list_adult,
					'required':	False,
				}
		}),
		('adult_doc_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Тип',
					'required':	False,
				}
		}),
		('adult_doc_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'min_length':	6,
					'required':	False,
				}
		}),
		('adult_doc_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Когда выдан',
					'required':	False,
				}
		}),
		('adult_doc_whom', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кем выдан',
					'required':	False,
				}
		}),
		('perm_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Тип',
					'choices':	list_perm,
					'required':	False,
				}
		}),
		('perm_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'min_length':	6,
					'required':	False,
				}
		}),
		('perm_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата принятия',
					'required':	False,
				}
		}),
		('perm_whom', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кем выдан',
					'required':	False,
				}
		}),
		('perm_due', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Срок действия разрешения',
					'required':	False,
				}
		}),
		('perm_due_vnz', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Действителен по',
					'help_text':	'для ВНЖ',
					'required':	False,
				}
		}),
	]),
	K_T_S:	SortedDict([
		('okved', {
				K_T_FIELD_A:	{
					'label':	'ОКВЭДы',
					'help_text':	'Чиста ОКВЭДы',
				},
				K_T_FIELD_T:	SortedDict([
					('code', {	# will be prefix
							K_T_FIELD_T:	K_MODEL_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Код',
								'queryset':	Okved.objects.exclude(parent=None).order_by('id'),
								'empty_label':	None,
							}
					}),
				]),
		}),
	]),
	K_T_T:	{		# templates description
		K_T_T_FORM:	'form/z0002.html',
		K_T_T_VIEW:	'print/z0002.xhtml',
		K_T_T_PRINT:	'print/z0002.xhtml',
	},
	'example':	(
		{
			'name': 	'min',
			'title':	'Минимальный',
			'data': {
				'spro_name':	'Межрайонную Инспекцию ФНС России № 15 по Санкт-Петербургу',
				'spro_id':	78086,
				'lastname':	'Иванов',
				'firstname':	'Иван',
				'midname':	'Иванович',
				'sex':		'мужской',
				'adult':	True,
				'birthdate':	'01.01.1970',
				'birthplace':	'Поребрик-сити',
				'addr_zip':	'192001',
				'addr_srf':	78,
				'addr_street':	'Ивановская',
				'addr_house':	'1',
				'doc_type':	'паспорт гражданина РФ',
				'doc_series':	'4005',
				'doc_no':	'654987',
				'doc_date':	'01.02.2003',
				'doc_whom':	'15 ОМ УМВД по Санкт-Петербургу',
				'doc_kp':	'789456'
			}
		},
		{
			'name': 	'max',
			'title':	'Максимальный',
			'data': {
				'spro_name':	'Межрайонную Инспекцию ФНС России № 15 по Санкт-Петербургу',
				'spro_id':	78086,
				'lastname':	'Сирко',
				'firstname':	'Проня',
				'midname':	'Прокоповна',
				'sex':		'женский',
				'adult':	False,
				'birthdate':	'08.03.1994',
				'birthplace':	'Киев',
				'inn':		'123456789012',
				'citizenship':	2,
				'country':	'Украина',
				'addr_zip':	'192001',
				'addr_srf':	78,
				'addr_region':	'Курортный р-н',
				'addr_locality':	'г.Зеленогорск',
				'addr_street':	'Садовая',
				'addr_house':	'1',
				'addr_building':	'лит.А',
				'addr_app':	'пом. 2Н',
				'phone_code':	'921',
				'phone_no':	'1234567',
				'phone_fax':	'9876543',
				'doc_type':	'паспорт',
				'doc_no':	'AX123456',
				'doc_date':	'01.02.2003',
				'doc_whom':	'МИД Украины',
				'adult_type':	2,
				'adult_doc_type':	'Свидетельство о браке',
				'adult_doc_no':	'654987',
				'adult_doc_date':	'01.02.2012',
				'adult_doc_whom':	'ЗАГС Зеленогорска',
				'perm_type':	1,
				'perm_no':	'134687',
				'perm_date':	'11.11.2011',
				'perm_whom':	'УФМС по г.Зеленогорск',
				'perm_due':	'11.11.2016',
				'perm_due_vnz':	'11.11.2011',
			}
		},
	),
}

def	__pre_vp(data):
	'''
	Private func for preparing data befor printing/previewing; add ocved_count
	'''
	data['okved_count'] = len(data['okved']) if 'okved' in data else 0
	okved_pages = list()
	okved_page = list()
	for n, c in enumerate(data['okved']):
		okved_page.append((n+1, c['code']))
		if ((n % 10) == 9):     # flush
			okved_pages.append(tuple(okved_page))
			okved_page = list()
	if (okved_page):                # flush tail
		okved_pages.append(okved_page)
	data['okved_pages'] = tuple(okved_pages)

def	PRE_VIEW(data):
	__pre_vp(data)

def	PRE_PRINT(data):
	__pre_vp(data)

def	PRE_SAVE(data):
	data['addr_srf'] = data['addr_srf'].pk
	for i, okved in enumerate(data['okved']):
		data['okved'][i]['code'] = okved['code'].pk

def	POST_LOAD(data):	# K_T_F_POST_LOAD
	data['addr_srf'] = SSRF.objects.get(pk = data['addr_srf'])
	for i, okved in enumerate(data['okved']):
		data['okved'][i]['code'] = Okved.objects.get(pk = okved['code'])

def	PRE_FORM(data):
	PRE_SAVE(data)
