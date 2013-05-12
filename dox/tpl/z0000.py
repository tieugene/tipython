# -*- coding: utf-8 -*-
'''
'''
from django.utils.datastructures import SortedDict
import sys
from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')


DATA = {
	K_T_UUID: '58ACC2A6E62C4574B3BE91475D5ACB98',
	K_T_NAME: 'Пример',
	K_T_FIELD:	SortedDict([]),
	K_T_T:	{
		K_T_T_PRINT:	'print/z0000.html',
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
