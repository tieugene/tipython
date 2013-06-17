# -*- coding: utf-8 -*-
'''
Форма 26.2-1 (переход на УСН)

[ИНН]:
[КПП]
КНО - int(4)
Признак: list (1..3)
Наименование организации / ФИО ИП: str(16)
c - list 1..3 (+[mon], year
Объект налогообложения: 1..2
Год подачи заи: int
Получено доходов за 9 мес: digit
Средняя численность работников за девять месяцев года подачи заявления: digit(3)
Стоимост имущества: int
Телефон
Кто подал: 1..2
ФИО руководителя/представителя: str(60)
Дата: date
Наименование документа: str(40)
'''

__legend = '''\
<p Регламентируется Приказом ФНС России от 13.04.2010 N ММВ-7-3/182@ </p>\
<p> Заявление об УСН (упрощенку), заявление о переходе на УСН - заполняется как существующими так и создаваемыми организациями или ИП (если они выбрали этот режим налогообложения). </p>\
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

app_sign_list = [
	(1, 'Сначала'),
	(2, '5 дней'),
	(3, 'Переход'),
]

chg_type_list = [
	(1, '1 января'),
	(2, 'Даты постановки на учет'),
	(3, '01.xx.21xx'),
]

tax_obj_list = [
	(1, 'Доходы'),
	(2, 'Доходы - расходы'),
]

app_type_list = [
	(1, 'Налогоплательщик'),
	(2, 'Представитель налогоплательщика'),
]

DATA = {
	K_T_UUID:	'D6A364487A1E4E7F853BCC4CA47B4E8D',
	K_T_NAME:	'Форма 26.2-1',
	K_T_COMMENTS:	'Заявление о переходе на упрощенную систему налогообложения (форма 11500010 по КНД)',
	K_T_LEGEND:	__legend,
	K_T_FIELD:	SortedDict([
		('inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'required':	False,
				}
		}),
		('kpp', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'КПП',
					'min_length':	9,
					'max_length':	9,
					'required':	False,
				}
		}),
		('kno', {
				K_T_FIELD_T:	K_CHAR_FIELD,	# FIXME: СОУН http://www.gnivc.ru/inf_provision/classifiers_reference/soun/
				K_T_FIELD_A:	{
					'label':	'КНО',
					'min_length':	4,
					'max_length':	4,
					'help_text':	'Код налогового органа',
				}
		}),
		('app_sign', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Признак заявителя',
					'choices':	app_sign_list,
				}
		}),
		('org_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Наименование организации',
					'max_length':	160,
					'help_text':	'Наименование организации / ФИО ИП',
				}
		}),
		('chg_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Переход на УСН с',
					'choices':	chg_type_list,
				}
		}),
		('chg_month', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'месяц',
					'min_value':	1,
					'max_value':	12,
					'required':	False,
				}
		}),
		('chg_year', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'год',
					'min_value':	2010,
					'max_value':	2099,
					'required':	False,
				}
		}),
		('tax_obj', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Объект н/о',
					'choices':	tax_obj_list,
					'help_text':	'Объект налогообложения',
				}
		}),
		('petition_year', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'Год подачи заявления',
					'min_value':	2010,
					'max_value':	2099,
				}
		}),
		('income', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'Доходы',
					'max_value':	999999999,
					'required':	False,
				}
		}),
		('workers', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'Работников',
					'max_value':	999,
					'required':	False,
				}
		}),
		('property', {
				K_T_FIELD_T:	K_INT_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имущество',
					'max_value':	999999999,
					'required':	False,
				}
		}),
		('phone', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Телефон',
					'max_length':	20,
					'required':	False,
				}
		}),
		('app_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Заявитель',
					'choices':	app_type_list,
				}
		}),
		('delegate_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Представитель',
					'max_length':	60,
					'required':	False,
				}
		}),
		('delegate_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата',
				}
		}),
		('delegate_doc', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Документ',
					'max_length':	40,
					'required':	False,
				}
		}),
	]),
	K_T_T:	{
		#K_T_T_FORM:	'form/z0007.html',
		K_T_T_PRINT:	'print/z0007.xfdf',
	},
	'example':	(
		{
			'name': 	'sample1',
			'title':	'Пример №1',
			'data': {
				'inn':		'1234567894',
				'kno':		'7801',
				'org_name':	'Остап Сулейман Ибрагим Берта Мария Бендер бей',
				'chg_year':	datetime.date.today().year,
				'petition_year':	datetime.date.today().year,
			}
		},
	),
}
