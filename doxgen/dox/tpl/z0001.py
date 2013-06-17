# -*- coding: utf-8 -*-
'''
Заявление
'''

# 1. django
from django import forms
from django.utils.datastructures import SortedDict
from django.contrib.admin.widgets import AdminDateWidget
# 2. 3rd party
# 3. system
import os, sys, pprint, datetime
# 4. my
import utils
from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')

__joke = '''Дорогой начальник. В течение этого года я тщетно пытался вырваться из ваших цепких лап. Каждый божий день я уходил, как только закончу очередной проект. Каждый божий день оказывалось, что проект я начинал с хвоста и поэтому не надо проектовой мордой мне в харю тыкать. Каждый из 365 дней этого гребаного года оказывался "самым неподходящим днем для того чтобы уйти в отпуск". Вся эта ситуация довела меня до того, что я горько смеюсь когда слышу, что крепостное право в России было отменено давным-давно. Вы понимаете, что рингтон вашего вызова (Хрюканье свиньи в последние два месяца - если вы не знали) вызывает у меня физическую боль? Но с сегодняшнего дня - все изменилось! Я украл вашу жену! Она у меня в заложницах!\
Мои условия:\
1) Две недели отпуска.\
2) Материальная помощь к отпуску в размере 5 окладов.\
3) Путевка на 10 дней в Сан Педро де Алькантара, в аппартаменты, которые я укажу позднее. На двоих (не ваша жена).\
Не пытайтесь связаться с милицией.\
Я вчера рассказал вашей жене о причинах моего поступка. Она долго плакала, а потом велела вам передать:\
"Если ты свяжешься с милицией - я тебе пупок развяжу, деспот!"'''

DATA = {
	K_T_UUID:	'2E4743DC1BAF48F1850362A655DF4D3F',	# generated with uuid.uuid4().hex.upper()
	K_T_NAME:	'Заявление',
	K_T_COMMENTS:	'Простое заявление общего вида',
	K_T_FIELD:	SortedDict([	# fields description
		('acceptor', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кому',
					'help_text':	'Должность, ФИО (в дательном падеже)',
				}
		}),
		('donor', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кого',
					'help_text':	'Должность, ФИО (в родительном падеже)',
				}
		}),
		('date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата',
					'help_text':	'ДД.ММ.ГГГГ',
					'widget':	AdminDateWidget,
				}
		}),
		('text', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Текст',
					'widget':	forms.Textarea,
				}
		}),
	]),
	K_T_T:	{		# templates description
		K_T_T_PRINT:	'print/z0001.html',
	},
	'example':	(
		{
			'name': 	'sample',
			'title':	'Пример №1',
			'tip':		'Шутка юмора',
			'data': {
				'acceptor':	'Генеральному директору ООО "Рога и Копыта" Иванову И. И.',
				'donor':	'Местного айтишника Петрова П. П.',
				'date':		datetime.date.today().strftime('%d.%m.%Y'),
				'text':		__joke,
			}
		},
	),
}

def	PRE_PRINT(data):
	data['text'] = data['text'].split('\n')

def	PRE_VIEW(data):
	PRE_PRINT(data)
