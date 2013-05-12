# -*- coding: utf-8 -*-

'''
It seems that _nested_ formsets are too hard to aprove.
So - solution is:
	* just 1 level of formsets
	* form - separately, formset[s] - separately
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

reload(sys)
sys.setdefaultencoding('utf-8')

DATA = {
	K_T_UUID:	'C9B0FA3ACED04F5E88131626A3881BBF',
	K_T_NAME:	'Форма 21001',
	K_T_COMMENTS:	'Заявление на регистрацию ИП',
	K_T_FIELD:	SortedDict([
		('lastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Фамилия',
					'initial':	'Иванов',
				}
		}),
		('firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имя',
					'initial':	'Иван',
				}
		}),
		('midname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Отчество',
					'initial':	'Иванович',
				}
		}),
		('sex', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'пол',
				}
		}),
		('birthdate', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата',
					'help_text':	'ДД.ММ.ГГГГ',
					'initial':	datetime.date.today(),
				}
		}),
		('birthplace', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место рождения',
					'initial':	'Поребрик-сити',
				}
		}),
		('addr_zip', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Индекс',
				}
		}),
		('addr_srf', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Субъект РФ',
					'initial':	'г. Санкт-Петербург',
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
					'label':	'Телефон: Код',
					'required':	False,
				}
		}),
		('phone_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Телефон: Номер',
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
		('doc_series', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ: Серия',
					'min_length':	4,
					'max_length':	4,
				}
		}),
		('doc_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ: Номер',
					'min_length':	6,
					'max_length':	6,
				}
		}),
		('doc_date', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ: Когда выдан (ДД.ММ.ГГГГ)',
				}
		}),
		('doc_whom', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ: Кем выдан',
				}
		}),
		('doc_kp', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ: Код подразделения',
					'min_length':	6,
					'max_length':	6,
				}
		}),
		('inn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'min_length':	12,
					'max_length':	12,
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
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Код',
							}
					}),
					('name', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Наименование',
							}
					}),
				]),
		}),
	]),
	K_T_T:	{		# templates description
		#K_T_T_LIST:	'list/z0001.html',
		K_T_T_FORM:	'form/z0002.html',
		#K_T_T_READ:	'view/z0001.html',
		K_T_T_VIEW:	'print/z0002.xhtml',
		K_T_T_PRINT:	'print/z0002.xhtml',
	}
}

def	__pre_vp(data):
	data['okved_count'] = len(data['okved']) if 'okved' in data else 0

def	PRE_VIEW(data):
	__pre_vp(data)

def	PRE_PRINT(data):
	__pre_vp(data)
