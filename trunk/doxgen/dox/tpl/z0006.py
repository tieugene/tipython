# -*- coding: utf-8 -*-
'''
Реквизиты фирмы
'''

# 1. django
from django import forms
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.template import RequestContext

# 2. 3rd party

# 3. system
import sys, pprint, datetime

# 4. my
import utils
from consts import *
from dox.models import Okved

reload(sys)
sys.setdefaultencoding('utf-8')

DATA = {
	K_T_UUID:	'BA5117097230415485557D211DD9908D',
	K_T_NAME:	'Реквизиты фирмы',
	K_T_COMMENTS:	'',
	K_T_FIELD:	SortedDict([
		('orgname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Наименование',
				}
		}),
		('date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата регистрации',
					'help_text':	'ДД.ММ.ГГГГ',
				}
		}),
		('addr', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Юридический адрес',
				}
		}),
		('ogrn', {
				K_T_FIELD_T:	K_OGRN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ОГРН',
				}
		}),
		('inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'max_length':	10,
				}
		}),
		('kpp', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'КПП',
					'min_length':	9,
					'max_length':	9,
				}
		}),
		('okato', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ОКАТО',
					'min_length':	11,
					'max_length':	11,
				}
		}),
		('bank_rs', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'р/с. №',
					'min_length':	20,
					'max_length':	20,
				}
		}),
		('bank_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'р/с. Дата',
				}
		}),
		('bank_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Банк',
				}
		}),
		('bank_ks', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'к/с',
					'min_length':	20,
					'max_length':	20,
				}
		}),
		('bank_bik', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'БИК',
					'min_length':	9,
					'max_length':	9,
				}
		}),
	]),
	K_T_S:	SortedDict([
		('boss', {
				K_T_FIELD_A:	{
					'label':	'Директор',
				},
				K_T_FIELD_T:	SortedDict([
					('fio', {
							K_T_FIELD_T:	K_CHAR_FIELD,
							K_T_FIELD_A:	{
								'label':	'ФИО',
							}
					}),
					('date', {
							K_T_FIELD_T:	K_DATE_FIELD,
							K_T_FIELD_A:	{
								'label':	'с',
							}
					}),
				]),
		}),
		('okved', {
				K_T_FIELD_A:	{
					'label':	'ОКВЭДы',
					'help_text':	'Первый - основной',
				},
				K_T_FIELD_T:	SortedDict([
					('code', {
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
		#K_T_T_LIST:	'list/z0001.html',
		K_T_T_FORM:	'form/z0006.html',
		#K_T_T_READ:	'view/z0001.html',
		K_T_T_VIEW:	'print/z0006.xhtml',
		K_T_T_PRINT:	'print/z0006.xhtml',
	},
	'example':	(
		{
			'name': 	'sample1',
			'title':	'Пример №1',
			'data': {
				'orgname':	'ООО «Рога & Копыта»',
				'date':		'15.01.2012',
				'addr':		'190121, г. Поребрик-сити, ул. Садовая, д. 111/113, литер А, пом. 4Н',
				'ogrn':		'1107847309008',
				'inn':		'7839431554',
				'kpp':		'783901001',
				'okato':	'40262561000',
				'bank_rs':	'40702810303260008123',
				'bank_date':	'31.01.2012',
				'bank_name':	'Филиал №7806 ВТБ 24 (ЗАО) ДО №33 "Каменноостровский, 44"',
				'bank_ks':	'30101810300000000811',
				'bank_bik':	'044030811',
			}
		},
	),
}

def	PRE_SAVE(data):
	# hack/
	for boss in data['boss']:
		utils.date2str(boss, 'date')
	# /hack
	for i, okved in enumerate(data['okved']):
		data['okved'][i]['code'] = okved['code'].pk

def	POST_LOAD(data):	# K_T_F_POST_LOAD
	# hack/
	for boss in data['boss']:
		utils.str2date(boss, 'date')
	# /hack
	for i, okved in enumerate(data['okved']):
		data['okved'][i]['code'] = Okved.objects.get(pk = okved['code'])

def	PRE_FORM(data):
	PRE_SAVE(data)
