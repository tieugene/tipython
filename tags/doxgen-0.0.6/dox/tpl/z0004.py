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
					'initial':	'',
				}
		}),
		('organisation_add', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Адрес',
					'initial':	'',
				}
		}),
		('organisation_inn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН/КПП',
					'initial':	'',
				}
		}),
		('dov_n', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Доверенность №',
					'initial':	'',
				}
		}),
		('dov_s', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата выдачи',
					'initial':	datetime.date.today(),
				}
		}),
		('dov_po', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Срок действия',
					'initial':	datetime.date.today(),
				}
		}),
		('postav', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Наименование поставщика',
					'initial':	'',
				}
		}),
		('schet_n', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'№ счёта',
					'initial':	'',
				}
		}),
		('dov_user', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Доверенность выдана',
					'initial':	'',
				}
		}),
		('dov_user_pass', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Паспорт',
					'initial':	'',
				}
		}),
		('dov_user_pass_vidan', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кем выдан',
					'initial':	'',
				}
		}),
		('dov_user_pass_date', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Когда выдан',
					'initial':	'',
				}
		}),
		('org_schet', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Счет организации',
					'initial':	'',
				}
		}),
	]),
	K_T_S:	SortedDict([
		('tova', {
				K_T_FIELD_A:	{
					'label':	'ОКВЭДы',
					'help_text':	'Чиста ОКВЭДы',
				},
				K_T_FIELD_T:	SortedDict([
					('nomer', {	# will be prefix
							K_T_FIELD_T:	K_CHAR_FIELD,	# ???
							K_T_FIELD_A:	{
								'label':	'Номер',
								'initial': '' ,
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
'''
class	OkvedForm(forms.Form):
	code		= forms.CharField(label='Код')
	name		= forms.CharField(label='Наименование')

OkvedFormSet = formset_factory(OkvedForm)

class	FORM(forms.Form):
	# Formsets: addr, phone, doc, okved
	name		= forms.CharField(label='Наименование')
	lastname	= forms.CharField(label='Фамилия', initial='Иванов')
	firstname	= forms.CharField(label='Имя', initial='Иван')
	midname		= forms.CharField(label='Отчество', required=False, initial='Иванович')
	#sex		= forms.ChoiceField(label='Пол', choices=dict_sex.items())
	birthdate	= forms.DateField(label='Дата рождения', help_text='формат: ДД.ММ.ГГГГ', initial='01.01.1970')
	birthplace	= forms.CharField(label='Место рождения', help_text='пример: гор. Поребрик-сити', initial='Санкт-Петербург')
	#citizenship	= forms.ChoiceField(label='Гражданство', choices=dict_citizenship.items())
	addr_zip	= forms.CharField(label='Индекс', initial='198001')
	#addr_srf	= forms.ChoiceField(label='Субъект РФ', choices=dict_srf.items(), initial='63')
	addr_region	= forms.CharField(label='Район', required=False)
	addr_city	= forms.CharField(label='Город', required=False, initial='г. Санкт-Петербург')
	addr_locality	= forms.CharField(label='Населенный пункт', required=False)
	addr_street	= forms.CharField(label='Улица', help_text='(проспект, переулок и т.д.)', initial='ул. Марата')
	addr_house	= forms.CharField(label='Дом', initial='дом 42')
	addr_building	= forms.CharField(label='Корпус (строение)', required=False)
	addr_app	= forms.CharField(label='Квартира (офис)', required=False)
	phone_code	= forms.CharField(label='Код', required=False)
	phone_no	= forms.CharField(label='Телефон', required=False)
	phone_fax	= forms.CharField(label='Факс', required=False)
	doc_series	= forms.CharField(label='Документ.Серия', initial='4005')
	doc_no		= forms.CharField(label='Документ.Номер', initial='123465')
	doc_date	= forms.CharField(label='Документ.Дата', initial='01.01.2003')
	doc_who		= forms.CharField(label='Документ.Кем выдан', initial='хез')
	doc_kp		= forms.CharField(label='Документ.Код подразделения', initial='789654')
	inn		= forms.CharField(label='ИНН', required=False, initial='7894561239871')
	#tax		= forms.ChoiceField(label='Налогообложение', choices=dict_tax.items(), initial='1')


def	ANON(request):
	bonus = {'form-TOTAL_FORMS': u'1', 'form-INITIAL_FORMS': u'0', 'form-MAX_NUM_FORMS': u'',}
	if request.method == 'POST':
		#form = FORM(request.POST)
		formset = formset_factory(OkvedForm)(request.POST)
                if formset.is_valid():
			pprint.pprint(formset.cleaned_data)	# list of dicts
			return utils.render_html2pdf(request, {'data': formset.cleaned_data}, DATA[K_T_T][K_T_T_PRINT])
		print "Invalid"
	else:	# GET
		#form = FORM()
		formset = formset_factory(OkvedForm)()
	return render_to_response(DATA[K_T_T][K_T_T_FORM], context_instance=RequestContext(request, {'formset': formset}))

def	PRE_SAVE(data):
	utils.date2str(data, 'birthdate')

def	POST_LOAD(data):
	print "Post load"
	#utils.str2date(data, 'birthdate')
'''
