# -*- coding: utf-8 -*-

import pprint

from django import forms
from django.utils.datastructures import SortedDict

from apps.models import *

class	DynaForm(forms.Form):
	name	= forms.CharField(label='Наименование фирмы (кратко)', help_text='пример: Ромашко')

	def __init__(self, *args, **kwargs):
		fieldlist = None
		if (kwargs.has_key('fieldlist')):
			fieldlist = kwargs['fieldlist']
			del(kwargs['fieldlist'])
		super(DynaForm, self).__init__(*args, **kwargs)
		if (fieldlist):
			for f in fieldlist:
				self.fields[f] = fieldlist[f]['t'](**fieldlist[f]['a'])

form = list()

formdata = (
	(	# 0001/
		SortedDict([
			('fss_no', {
					't':	forms.IntegerField,
					'a':	{
						'label':	'Филиал ФСС №',
						'help_text':	'пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»',
					}
			}),
			('opening', {
					't':	forms.BooleanField,
					'a':	{
						'label':	'Открытие',
						'required':	False,
					}
			}),
			('oname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Наименование фирмы (полное)',
						'help_text':	'пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»',
					}
			}),
			('oinn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН фирмы',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('okpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'КПП фирмы',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('ookato', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКАТО фирмы',
						'min_length':	8,
						'max_length':	11,
					}
			}),
			('oogrn', {
					't':	forms.CharField,
					'a':	{
						'label':	'Рег. №',
						'help_text':	'ОГРН, штоле?',
						'min_length':	10,
						'max_length':	16,
					}
			}),
			('bname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Полное наименование банка',
						'help_text':	'пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»',
					}
			}),
			('binn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН банка',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('bkpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'КПП банка',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('bogrn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОГРН банка',
						'min_length':	10,
						'max_length':	16,
					}
			}),
			('bik', {
					't':	forms.CharField,
					'a':	{
						'label':	'БИК',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('rs', {
					't':	forms.CharField,
					'a':	{
						'label':	'Р/с',
						'min_length':	20,
						'max_length':	20,
					}
			}),
			('jobrole', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Должность',
						'help_text':	'пример: Ген. директор',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss_fio', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Фамилия И. О.',
						'help_text':	'пример: Ген. директор',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('date0', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата закрытия/открытия',
						'help_text':	'пример: 27.09.2011',
					}
			}),
			('date1', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата документа',
					}
			}),
		]),
	),	# /0001
	(	# 0002/
		SortedDict([
			('opening', {
					't':	forms.BooleanField,
					'a':	{
						'label':	'Открытие',
						'required':	False,
					}
			}),
			('oname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Наименование фирмы (полное)',
						'help_text':	'пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»',
					}
			}),
			('oaddr', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес фирмы',
						'help_text':	'пример: 191187, Санкт-Петербург, ул. Шпалерная, д. 9, литер А, пом. 4-Н',
					}
			}),
			('oinn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН фирмы',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('opfrno', {
					't':	forms.CharField,
					'a':	{
						'label':	'Рег. № в ПФР',
						'min_length':	14,
						'max_length':	14,
					}
			}),
			('opfrname', {
					't':	forms.CharField,
					'a':	{
						'label':	'УПФР в',
						'help_text':	'пример: Центральном р-не г. Санкт-Петербурга',
					}
			}),
			('bname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Полное наименование банка',
						'help_text':	'пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»',
					}
			}),
			('baddr', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес банка',
					}
			}),
			('binn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН банка',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('bkpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'КПП банка',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('bik', {
					't':	forms.CharField,
					'a':	{
						'label':	'БИК',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('rs', {
					't':	forms.CharField,
					'a':	{
						'label':	'Р/с',
						'min_length':	20,
						'max_length':	20,
					}
			}),
			('jobrole', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Должность',
						'help_text':	'пример: Ген. директор',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Фамилия И. О.',
						'help_text':	'пример: Ген. директор',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('date0', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата закрытия/открытия',
						'help_text':	'пример: 27.09.2011',
					}
			}),
			('date1', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата документа',
					}
			}),
		]),
	),	# /0002
	(	# 0003/
		SortedDict([
			('opening', {
					't':	forms.BooleanField,
					'a':	{
						'label':	'Открытие',
						'required':	False,
					}
			}),
			('kno', {
					't':	forms.CharField,
					'a':	{
						'label':	'Код налогового органа',
						'min_length':	4,
						'max_length':	4,
					}
			}),
			('otype', {
					't':	forms.ChoiceField,
					'a':	{
						'label':	'Тип фирмы',
						'choices':	(('1', 'Российская'), ('2', 'Иностранная'), ('3', 'Иностранная через ОП'), ('4', 'ИП'), ('5', 'Нотариус')),
					}
			}),
			('oname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Наименование фирмы (полное)',
						'help_text':	'пример: Общество с ограниченной ответственностью «Торговый дом Ромашко»',
					}
			}),
			('oinn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН фирмы',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('okpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'КПП фирмы',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('oogrn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОГРН фирмы',
						'min_length':	10,
						'max_length':	16,
					}
			}),
			('jobrole', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Должность',
						'help_text':	'пример: Ген. директор',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss_f', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Фамилия',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss_i', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Имя',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss_o', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Отчество',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('boss_inn', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.ИНН',
						'min_length':	10,	# ?
						'max_length':	12,	# ?
					}
			}),
			('boss_phone', {
					't':	forms.CharField,
					'a':	{
						'label':	'Руководитель.Контактный телефон',
						'min_length':	6,
						'max_length':	20,
					}
			}),
			('rs', {
					't':	forms.CharField,
					'a':	{
						'label':	'Р/с',
						'min_length':	20,
						'max_length':	20,
					}
			}),
			('bank_name', {
					't':	forms.CharField,
					'a':	{
						'label':	'Полное наименование банка',
						'help_text':	'пример: Открытое акционерное общество «Санкт-Петербургский Индустриальный Акционерный Банк»',
					}
			}),
			('bank_inn', {
					't':	forms.CharField,
					'a':	{
						'label':	'ИНН банка',
						'min_length':	10,
						'max_length':	12,
					}
			}),
			('bank_kpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'КПП банка',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('bank_zip', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Индекс',
						'min_length':	6,
						'max_length':	6,
					}
			}),
			('bank_bik', {
					't':	forms.CharField,
					'a':	{
						'label':	'БИК',
						'min_length':	9,
						'max_length':	9,
					}
			}),
			('bank_reg', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Код региона',
						'min_length':	1,
						'max_length':	2,
					}
			}),
			('bank_addr_district', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Район',
						'required':	False,
					}
			}),
			('bank_addr_city', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Город',
					}
			}),
			('bank_addr_locality', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Населенный пункт',
						'required':	False,
					}
			}),
			('bank_addr_street', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Улица',
						'help_text':	'(проспект, переулок и т.д.)',
					}
			}),
			('bank_addr_building', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Дом',
						'help_text':	'(владение)',
					}
			}),
			('bank_addr_housing', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Корпус',
						'help_text':	'(строение)',
						'required':	False,
					}
			}),
			('bank_addr_office', {
					't':	forms.CharField,
					'a':	{
						'label':	'Банк.Адрес.Офис',
						'help_text':	'(помещение)',
						'required':	False,
					}
			}),
			('date0', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата закрытия/открытия',
						'help_text':	'пример: 27.09.2011',
					}
			}),
			('date1', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата документа',
					}
			}),
		]),
	),	# /0003
	(	# 0004/
		SortedDict([
			('org_name', {
					't':	forms.CharField,
					'a':	{
						'label':	'Наименование организации',
						'help_text':	'пример: «Торговый дом Ромашко» (с кавычками)',
					}
				}
			),
			('org_fokopf', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКОПФ (полностью)',
						'help_text':	'пример: Общество с ограниченной ответственностью',
					}
				}
			),
			('org_sokopf', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКОПФ (кратко)',
						'help_text':	'пример: ООО',
					}
				}
			),
			('org_ffname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Полное наименование на иностранном языке',
						'help_text':	'пример: Romashka, Ltd.',
						'required':	False
					}
				}
			),
			('org_fsname', {
					't':	forms.CharField,
					'a':	{
						'label':	'Краткое наименование на иностранном языке',
						'required':	False
					}
				}
			),
			('org_addr_zip', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Индекс',
					}
				}
			),
			('org_addr_subj', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Субъект Российской Федерации',
					}
				}
			),
			('org_addr_distinct', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Район',
						'required':	False
					}
				}
			),
			('org_addr_city', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Город',
						'required':	False
					}
				}
			),
			('org_addr_locality', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Населенный пункт',
						'required':	False,
					}
			}),
			('org_addr_street', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Улица',
						'help_text':	'(проспект, переулок и т.д.- указать нужное с наименованием)',
					}
			}),
			('org_addr_building_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Дом (тип)',
						'help_text':	'пример: дом',
					}
			}),
			('org_addr_building', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Дом',
						'help_text':	'(владение)',
					}
			}),
			('org_addr_housing_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Корпус (тип)',
						'help_text':	'пример: лит.',
						'required':	False,
					}
			}),
			('org_addr_housing', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Корпус',
						'help_text':	'(строение)',
						'required':	False,
					}
			}),
			('org_addr_office_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Офис (тип)',
						'help_text':	'пример: пом.',
						'required':	False,
					}
			}),
			('org_addr_office', {
					't':	forms.CharField,
					'a':	{
						'label':	'Адрес.Офис',
						'help_text':	'(помещение)',
						'required':	False,
					}
			}),
			('org_fund', {
					't':	forms.IntegerField,
					'a':	{
						'label':	'Уставной фонд',
					}
			}),
			('org_asset', {
					't':	forms.CharField,
					'a':	{
						'label':	'Имущество',
					}
			}),
			('org_date_solution', {
					't':	forms.DateField,
					'a':	{
						'label':	'Дата решения',
					}
			}),
			('founder_f', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Фамилия',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('founder_i', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Имя',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('founder_o', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Отчество',
						'min_length':	4,
						'max_length':	20,
					}
			}),
			('founder_birthdate', {
					't':	forms.DateField,
					'a':	{
						'label':	'Учредитель.Дата рождения',
					}
			}),
			('founder_birthplace', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Место рождения',
					}
			}),
			('founder_inn', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.ИНН',
						'min_length':	12,
						'max_length':	12,
						'required':	False,
					}
			}),
			('founder_doc_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Документ.Тип',
					}
			}),
			('founder_doc_series', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Документ.Серия',
					}
			}),
			('founder_doc_no', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Документ.Номер',
					}
			}),
			('founder_doc_date', {
					't':	forms.DateField,
					'a':	{
						'label':	'Учредитель.Документ.Дата',
					}
			}),
			('founder_doc_who', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Документ.Кем выдан',
					}
			}),
			('founder_doc_kp', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Документ.Код подразделения',
						'min_length':	7,
						'max_length':	7,
					}
			}),
			('founder_addr_zip', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Индекс',
						'min_length':	6,
						'max_length':	6,
					}
				}
			),
			('founder_addr_subj', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Субъект Российской Федерации',
					}
				}
			),
			('founder_addr_distinct', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Район',
						'required':	False
					}
				}
			),
			('founder_addr_city', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Город',
						'required':	False
					}
				}
			),
			('founder_addr_locality', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Населенный пункт',
						'required':	False,
					}
			}),
			('founder_addr_street', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Улица',
						'help_text':	'(проспект, переулок и т.д.- указать нужное с наименованием)',
					}
			}),
			('founder_addr_building_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Дом (тип)',
						'help_text':	'пример: дом',
					}
			}),
			('founder_addr_building', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Дом',
						'help_text':	'(владение)',
					}
			}),
			('founder_addr_housing_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Корпус (тип)',
						'help_text':	'пример: лит.',
						'required':	False,
					}
			}),
			('founder_addr_housing', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Корпус',
						'help_text':	'(строение)',
						'required':	False,
					}
			}),
			('founder_addr_office_type', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Офис (тип)',
						'help_text':	'пример: пом.',
						'required':	False,
					}
			}),
			('founder_addr_office', {
					't':	forms.CharField,
					'a':	{
						'label':	'Учредитель.Адрес.Офис',
						'help_text':	'(помещение)',
						'required':	False,
					}
			}),
			('org_dov_fns', {
					't':	forms.CharField,
					'a':	{
						'label':	'Доверенные в ФМС',
						'help_text':	'Каждый - 1 строка: Гр. Фамилия Имя Отчество (в.п.), 01 января 1970 года рождения, паспорт... выдан (кем, где, когда, код подразделения)..., зарегистрированного по адресу... ',
						'widget': forms.Textarea,
					}
			}),
			('org_dov_pf', {
					't':	forms.CharField,
					'a':	{
						'label':	'Доверенные в ПФ',
						'help_text':	'Каждый - 1 строка: Фамилия Имя Отчество (и.п.), 01 января 1970 года рождения, паспорт... выдан (кем, где, когда, код подразделения)..., зарегистрированного по адресу... ',
						'widget': forms.Textarea,
					}
			}),
			('org_pages_F11001', {
					't':	forms.IntegerField,
					'a':	{
						'label':	'Страниц в Форме 11001',
						'required':	False,
					}
			}),
			('org_pages_charter', {
					't':	forms.IntegerField,
					'a':	{
						'label':	'Страниц в Уставе',
						'required':	False,
					}
			}),
			('org_inn', {
					't':	forms.CharField,
					'a':	{
						'label':	'Организация.ИНН',
						'min_length':	10,
						'max_length':	10,
						'required':	False,
					}
			}),
			('org_kpp', {
					't':	forms.CharField,
					'a':	{
						'label':	'Организация.КПП',
						'min_length':	9,
						'max_length':	9,
						'required':	False,
					}
			}),
			('org_ogrn', {
					't':	forms.CharField,
					'a':	{
						'label':	'Организация.ОГРН',
						'min_length':	13,
						'max_length':	13,
						'required':	False,
					}
			}),
			('org_date_reg', {
					't':	forms.DateField,
					'a':	{
						'label':	'Организация.Дата регистрации',
						'required':	False,
					}
			}),
			('org_okveds', {
					't':	forms.IntegerField,
					'a':	{
						'label':	'ВЭДов',
					}
			}),
			('org_okved_00_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 0',
						'min_length':	4,
						'max_length':	8,
					}
			}),
			('org_okved_00_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 0',
					}
			}),
			('org_okved_01_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 1',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_01_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 1',
						'required':	False,
					}
			}),
			('org_okved_02_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 2',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_02_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 2',
						'required':	False,
					}
			}),
			('org_okved_03_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 3',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_03_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 3',
						'required':	False,
					}
			}),
			('org_okved_04_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 4',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_04_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 4',
						'required':	False,
					}
			}),
			('org_okved_05_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 5',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_05_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 5',
						'required':	False,
					}
			}),
			('org_okved_06_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 6',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_06_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 6',
						'required':	False,
					}
			}),
			('org_okved_07_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 7',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_07_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 7',
						'required':	False,
					}
			}),
			('org_okved_08_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 8',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_08_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 8',
						'required':	False,
					}
			}),
			('org_okved_09_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 9',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_09_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 9',
						'required':	False,
					}
			}),
			('org_okved_10_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 10',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_10_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 10',
						'required':	False,
					}
			}),
			('org_okved_11_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 11',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_11_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 11',
						'required':	False,
					}
			}),
			('org_okved_12_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 12',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_12_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 12',
						'required':	False,
					}
			}),
			('org_okved_13_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 13',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_13_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 13',
						'required':	False,
					}
			}),
			('org_okved_14_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 14',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_14_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 14',
						'required':	False,
					}
			}),
			('org_okved_15_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 15',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_15_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 15',
						'required':	False,
					}
			}),
			('org_okved_16_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 16',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_16_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 16',
						'required':	False,
					}
			}),
			('org_okved_17_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 17',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_17_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 17',
						'required':	False,
					}
			}),
			('org_okved_18_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 18',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_18_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 18',
						'required':	False,
					}
			}),
			('org_okved_19_k', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Код № 19',
						'min_length':	4,
						'max_length':	8,
						'required':	False,
					}
			}),
			('org_okved_19_v', {
					't':	forms.CharField,
					'a':	{
						'label':	'ОКВЭД.Наименование № 19',
						'required':	False,
					}
			}),
		]),
	),	# /0004
)

def	genform():
	'''
	Fillout form list
	'''
	pass
	#for f in formdata:
