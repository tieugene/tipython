# -*- coding: utf-8 -*-

# 1. django
from django import forms
from django.utils.datastructures import SortedDict
# 2. 3rd party
# 3. system
import os, sys, pprint, datetime
# 4. my
import utils
from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')

__joke = '''Дорогой начальник. В течение этого года я тщетно пытался вырваться из ваших цепких лап. Каждый божий день я уходил, как только закончу очередной проект. Каждый божий день оказывалось, что проект я начинал с хвоста и поэтому не надо проектовой мордой мне в харю тыкать. Каждый из 365 дней этого гребаного года оказывался "самым неподходящим днем для того чтобы уйти в отпуск". Вся эта ситуация довела меня до того, что я горько смеюсь когда слышу, что крепостное право в России было отменено давным-давно. Вы понимаете, что рингтон вашего вызова (Хрюканье свиньи в последние два месяца - если вы не знали) вызывает у меня физическую боль? Но с сегодняшнего дня - все изменилось! Я украл вашу жену! Она у меня в заложницах!
Мои условия:
1) Две недели отпуска.
2) Материальная помощь к отпуску в размере 5 окладов.
3) Путевка на 10 дней в Сан Педро де Алькантара, в аппартаменты, которые я укажу позднее. На двоих (не ваша жена).
Не пытайтесь связаться с милицией.
Я вчера рассказал вашей жене о причинах моего поступка. Она долго плакала, а потом велела вам передать:
"Если ты свяжешься с милицией - я тебе пупок развяжу, деспот!"'''

DATA = {
	K_T_UUID:	'2E4743DC1BAF48F1850362A655DF4D3F',	# generated with uuid.uuid4().hex.upper()
	K_T_NAME:	'Заявление',
	K_T_COMMENTS:	'Каменты',
	K_T_FIELD:	SortedDict([	# fields description
		('acceptor', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кому',
					'help_text':	'Должность, ФИО (в дательном падеже)',
					'initial':	'Генеральному директору ООО "Рога и Копыта" Иванову И. И.',
				}
		}),
		('donor', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Кого',
					'help_text':	'Должность, ФИО (в родительном падеже)',
					'initial':	'Местного айтишника Петрова П. П.',
				}
		}),
		('date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата',
					'help_text':	'ДД.ММ.ГГГГ',
					'initial':	datetime.date.today(),
				}
		}),
		('text', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Текст',
					'widget':	forms.Textarea,
					'initial':	__joke,
				}
		}),
	]),
	K_T_T:	{		# templates description
		#K_T_T_LIST:	'list/z0001.html',
		#K_T_T_FORM:	'form/z0001.html',
		#K_T_T_VIEW:	'view/z0001.html',
		K_T_T_PRINT:	'print/z0001.html',
	}
}

def	PRE_PRINT(data):
	data['text'] = data['text'].split('\n')
