# -*- coding: utf-8 -*-
'''
Форма ПД-4сб (Квитанция на оплату в Сбербанке (налог))
'''

__legend = '''\
<p> Квитанция предназначена для оплаты налогов и сборов и отличается от ПД-4 наличием КБК. </p>\
<p> Есть примеры заполнения для оплаты регистрации ИП и ООО. </p>\
'''

from django.utils.datastructures import SortedDict
from django.forms.extras.widgets import SelectDateWidget

# 3. system
import sys, datetime

from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')

DATA = {
	K_T_UUID:	'98A391C4F45C4A2AA21A69E6C16592EC',
	K_T_NAME:	'Форма ПД-4сб',
	K_T_COMMENTS:	'Квитанция на оплату в Сбербанке (налог)',
	K_T_LEGEND:	__legend,
	K_T_FIELD:	SortedDict([
		('recipient', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Получатель',
				}
		}),
		('recishort', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Получатель (кратко)',
				}
		}),
		('inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
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
		('account', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Р/С',
					'min_length':	20,
					'max_length':	20,
				}
		}),
		('bank', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Банк',
				}
		}),
		('bik', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'БИК',
					'min_length':	8,
					'max_length':	9,
				}
		}),
		('ks', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кор. счет',
					'required':	False,
					'min_length':	20,
					'max_length':	20,
				}
		}),
		('kbk', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'КБК',
					'min_length':	20,
					'max_length':	20,
				}
		}),
		('details', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Назначение',
				}
		}),
		('payer_fio', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Плательщик',
				}
		}),
		('payer_address', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Адрес',
				}
		}),
		('payer_inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН плательщика',
					'required':	False,
					'min_length':	12,
				}
		}),
		('total', {
				K_T_FIELD_T:	K_CHAR_FIELD,	# K_DEC_FIELD
				K_T_FIELD_A:	{
					'label':	'Сумма',
					#'decimal_places':	2,
				}
		}),
		('date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата',
					'required':	False,
					'widget':	SelectDateWidget,
				}
		}),
	]),
	K_T_T:	{
		K_T_T_FORM:	'form/z0003.html',
		K_T_T_VIEW:	'print/z0003.html',
		K_T_T_PRINT:	'print/z0003.html',
	},
	'example':	(
		{
			'name': 	'ip',
			'title':	'ИП',
			'tip':		'Заполнение для оплаты открытия ИП',
			'data': {
				'recipient':	'МИ ФНС РФ №11 по Санкт-Петербургу',
				'recishort':	'УФК МФ РФ по СПб',
				'inn':		'7842000011',
				'kpp':		'784201001',
				'okato':	'40298564000',
				'account':	'40101810200000010001',
				'bank':		'ГРКЦ ГУ Банка России по Санкт-Петербургу',
				'bik':		'044030001',
				'payer_fio':	'Иванов Иван Иванович',
				'payer_address':	'г.Санкт-Петербург, ул.Садовая, 1',
				'kbk':		'18210807010011000110',
				'details':	'за государственную регистрацию физ.лиц, ИП',
				'total':	'800.00',
				'date':		datetime.date.today().strftime('%d.%m.%Y'),
			}
		},
		{
			'name':		'ltd',
			'title':	'ООО',
			'tip':		'Заполнение для оплаты открытия ООО',
			'data': {
				'recipient':	'МИ ФНС РФ №11 по Санкт-Петербургу',
				'recishort':	'УФК МФ РФ по СПб',
				'inn':		'7842000011',
				'kpp':		'784201001',
				'okato':	'40298564000',
				'account':	'40101810200000010001',
				'bank':		'ГРКЦ ГУ Банка России по Санкт-Петербургу',
				'bik':		'044030001',
				'kbk':		'18210807010011000110',
				'details':	'за государственную регистрацию юр.лиц',
				'total':	'4000.00',
				'date':		datetime.date.today().strftime('%d.%m.%Y'),
			}
		},
	)
}
