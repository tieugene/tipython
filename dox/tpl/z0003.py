# -*- coding: utf-8 -*-
'''
'''
from django.utils.datastructures import SortedDict
# 3. system
import sys, datetime

from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')


DATA = {
	K_T_UUID:	'98A391C4F45C4A2AA21A69E6C16592EC',
	K_T_NAME:	'Форма ПД-4',
	K_T_COMMENTS:	'Квитанция на оплату в Сбербанке (налог)',
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
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'min_length':	10,
					'max_length':	12,
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
					'initial':	'Иванов Иван Иванович',
				}
		}),
		('payer_address', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Адрес',
					'initial':	'г. Санкт-Петербург, ул. Марата, дом 42',
				}
		}),
		('payer_inn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН плательщика',
					'required':	False,
					'min_length':	12,
					'max_length':	12,
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
					'initial':	datetime.date.today(),
				}
		}),
	]),
	K_T_T:	{
		K_T_T_FORM:	'form/z0003.html',
		K_T_T_VIEW:	'print/z0003.html',
		K_T_T_PRINT:	'print/z0003.html',
	}
}
