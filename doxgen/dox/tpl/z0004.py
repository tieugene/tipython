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
import os, sys, pprint, datetime

# 4. my
import utils
from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')
now_date = datetime.date.today()
delta = datetime.timedelta(days=10)
new_date = now_date + delta
DATA = {
	K_T_UUID:	'432688ED137E40BCAADBB1F6CB092ABC',
	K_T_NAME:	'Доверенность форма м2',
	K_T_COMMENTS:	'Доверенность на получение материальных ценностей',
	K_T_FIELD:	SortedDict([
		('organisation', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Организация',
				}
		}),
		('organisation_add', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Адрес',
				}
		}),
		('organisation_inn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН/КПП',
				}
		}),
		('dov_n', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Доверенность №',
				}
		}),
		('dov_s', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата выдачи',
				}
		}),
		('dov_po', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Срок действия',
				}
		}),
		('postav', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Наименование поставщика',
				}
		}),
		('schet_n', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'№ счёта',
				}
		}),
		('dov_user', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Доверенность выдана',
				}
		}),
		('dov_user_pass', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Паспорт',
				}
		}),
		('dov_user_pass_vidan', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кем выдан',
				}
		}),
		('dov_user_pass_date', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Когда выдан',
				}
		}),
		('org_schet', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Счет организации',
				}
		}),
	]),
	K_T_S:	SortedDict([
		('tova', {
				K_T_FIELD_A:	{
					'label':	'Товары',
					'help_text':	'Чиста товары',
				},
				K_T_FIELD_T:	SortedDict([
					('nomer', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Номер',
							}
					}),
					('naim', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Наименование',
							}
					}),
					('ed_izm', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Еденица измерения',
							}
					}),
					('kolvo', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Количество',
							}
					}),
					('kolvo_prop', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Количество прописью',
							}
					}),
				]),
		}),
	]),
	K_T_T:	{		# templates description
		#K_T_T_LIST:	'list/z0001.html',
		#K_T_T_FORM:	'form/z0002.html',
		#K_T_T_READ:	'view/z0001.html',
		K_T_T_VIEW:	'print/z0004.html',
		K_T_T_PRINT:	'print/z0004.html',
	}
}
