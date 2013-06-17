# -*- coding: utf-8 -*-
'''
Уведомление мигранта.
'''

__legend = '''\
<p> Уведомление о прибытии иностранного гражданина, уведомление мигранта - направляется в адрес ФМС для постановки мигранта на учет. Регламент постановки на учет иностранного гражданина, с помощью уведомления описан в следующих нормативных актах: </p>\
<ul>\
<li> Федеральный законом № 109-ФЗ от 18 июля 2006 года «О миграционном учете иностранных граждан и лиц без гражданства в Российской Федерации»</li>\
<li> Постановление Правительства РФ № 9 от 15.01.2007 г. «Правила осуществления миграционного учета иностранных граждан и лиц без гражданства в Российской Федерации»</li>\
<li> Постановление Правительства РФ № 10 от 15.01.2007 г. «Об установлении размера платы за услуги организаций федеральной почтовой связи по приему уведомления о прибытии иностранного гражданина или лица без гражданства в место пребывания на территории Российской Федерации»</li>\
</ul>\
<p> Вы можете заполнить его здесь, распечатать - и отнести в ближаешее отделение Почты России. </p>\
<p> <i> (не забудьте принимающую сторону с паспортом). </i> </p>\
'''

from django.utils.datastructures import SortedDict
# 3. system
import sys, datetime, pprint

from consts import *
from dox.models import SSRF

reload(sys)
sys.setdefaultencoding('utf-8')

list_sex = [
	(1, 'мужской'),
	(2, 'женский'),
]
list_visa = [
	(0, '---'),
	(1, 'Виза'), 
	(2, 'ВНЖ'),
	(3, 'РВП'),
]
list_aim = [
	(1, 'служебная'),
	(2, 'туризм'),
	(3, 'деловая'),
	(4, 'учеба'),
	(5, 'работа'),
	(6, 'частная'),
	(7, 'транзит'),
	(8, 'гуманитарная'),
	(9, 'другая'),
]
list_host = [
	(1, 'Физ. лицо'),
	(2, 'Организация'),
]

# http://blanker.ru/doc/migration-notification

DATA = {
	K_T_UUID:	'D886C413BCFF40CE8F7833A57673F3CF',
	K_T_NAME:	'Уведомление мигранта',
	K_T_COMMENTS:	'Уведомление о прибытии иностранного гражданина или лица без гражданства в место пребывания',
	K_T_LEGEND:	__legend,
	K_T_FIELD:	SortedDict([
		('m_lastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Фамилия',
					'max_length':	35,
				}
		}),
		('m_firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имя, Отчество',
					'max_length':	35,
				}
		}),
		('m_citizenship', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Гражданство, подданство',
					'max_length':	34,
				}
		}),
		('m_birthdate', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата рождения',
				}
		}),
		('m_sex', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Пол',
					'choices':	list_sex,
				}
		}),
		('m_birthcountry', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Государство рождения',
					'max_length':	33,
				}
		}),
		('m_birthlocation', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Город рождения',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('m_idcard_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Вид',
					'max_length':	11,
				}
		}),
		('m_idcard_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Серия',
					'max_length':	4,
				}
		}),
		('m_idcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'max_length':	9,
				}
		}),
		('m_idcard_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Выдан',
				}
		}),
		('m_idcard_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'До',
				}
		}),
		('m_visa_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Вид',
					'choices':	list_visa,
					'required':	False,
				}
		}),
		('m_visa_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Серия',
					'max_length':	4,
					'required':	False,
				}
		}),
		('m_visa_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'max_length':	9,
					'required':	False,
				}
		}),
		('m_visa_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Выдан',
					'required':	False,
				}
		}),
		('m_visa_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Виза.До',
					'required':	False,
				}
		}),
		('aim', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Цель въезда',
					'choices':	list_aim,
				}
		}),
		('profession', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Профессия',
					'max_length':	35,
					'required':	False,
				}
		}),
		('experience', {
				K_T_FIELD_T:	K_DEC_FIELD,
				K_T_FIELD_A:	{
					'label':	'Стаж',
					'required':	False,
				}
		}),
		('arrive', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата прибытия',
				}
		}),
		('expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Срок пребывания до',
				}
		}),
		('mcard_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Серия',
					'max_length':	4,
					'required':	False,
				}
		}),
		('mcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'max_length':	7,
					'required':	False,
				}
		}),
		('represent', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Сведения о законных представителях',
					'max_length':	95,
					'required':	False,
				}
		}),
		('seat_srf', {
				K_T_FIELD_T:	K_MODEL_FIELD,
				K_T_FIELD_A:	{
					'label':	'СРФ',
					'queryset':	SSRF.objects.all(),
					'empty_label':	None,
				}
		}),
		('seat_region', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Район',
					'max_length':	35,
					'required':	False,
				}
		}),
		('seat_city', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Город',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('seat_street', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Улица',
					'max_length':	35,
				}
		}),
		('seat_house', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дом',
					'max_length':	4,
				}
		}),
		('seat_housing', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Корпус',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_building', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Строение',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_flat', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Квартира',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_phone', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Телефон',
					'max_length':	10,
					'required':	False,
				}
		}),
		('host_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Принимающая сторона',
					'choices':	list_host,
				}
		}),
		('h_lastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Фамилия',
					'max_length':	35,
				}
		}),
		('h_firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Имя, Отчество',
					'max_length':	35,
				}
		}),
		('h_birthdate', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дата рождения',
				}
		}),
		('h_idcard_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Вид',
					'max_length':	11,
				}
		}),
		('h_idcard_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Серия',
					'max_length':	4,
				}
		}),
		('h_idcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Номер',
					'max_length':	9,
				}
		}),
		('h_idcard_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Выдан',
				}
		}),
		('h_idcard_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'До',
				}
		}),
		('h_srf', {
				K_T_FIELD_T:	K_MODEL_FIELD,
				K_T_FIELD_A:	{
					'label':	'СРФ',
					'queryset':	SSRF.objects.all(),
					'empty_label':	None,
				}
		}),
		('h_region', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Район',
					'max_length':	35,
					'required':	False,
				}
		}),
		('h_city', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Город',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('h_street', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Улица',
					'max_length':	35,
				}
		}),
		('h_house', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Дом',
					'max_length':	4,
				}
		}),
		('h_housing', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Корпус',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_building', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Строение',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_flat', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Квартира',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_phone', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Телефон',
					'max_length':	10,
					'required':	False,
				}
		}),
		('org_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Наименование',
					'max_length':	52,
					'required':	False,
				}
		}),
		('org_addr', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Факт. адрес',
					'max_length':	52,
					'required':	False,
				}
		}),
		('org_inn', {
				K_T_FIELD_T:	K_INN_FIELD,
				K_T_FIELD_A:	{
					'label':	'ИНН',
					'min_length':	12,
					'required':	False,
				}
		}),
	]),
	K_T_T:	{
		K_T_T_FORM:	'form/z0005.html',
		K_T_T_PRINT:	'print/z0005.xfdf',
	},
	'example':	(
		{
			'name': 	'sample1',
			'title':	'Остап Бендер',
			'data': {
				'm_lastname':		'Бендер Бей',
				'm_firstname':		'Остап Сулейман Берта Мария',
				'm_citizenship':	'Украина',
				'm_birthdate':		'01.01.1900',
				'm_birthcountry':	'Украина',
				'm_birthlocation':	'г.Одесса',
				'm_idcard_type':	'паспорт',
				'm_idcard_sn':		'AX',
				'm_idcard_no':		'880666',
				'm_idcard_date':	'01.03.2003',
				'm_idcard_expired':	'01.03.2013',
				'arrive':		datetime.date.today().strftime('%d.%m.%Y'),
				'expired':		(datetime.date.today() + datetime.timedelta(90)).strftime('%d.%m.%Y'),
				'seat_srf':		77,
				'seat_city':		'Нерезиновая',
				'seat_street':		'пер. Сивцев Вражек',
				'seat_house':		'27',
				'h_lastname':		'Иванопуло',
				'h_firstname':		'Николай',
				'h_birthdate':		'02.02.1902',
				'h_idcard_type':	'паспорт',
				'h_idcard_sn':		'4005',
				'h_idcard_no':		'123456',
				'h_idcard_date':	'01.02.2003',
				'h_idcard_expired':	'01.02.2013',
				'h_srf':		78,
				'h_city':		'Поребрик-сити',
				'h_street':		'Садовая',
				'h_house':		'111',
			}
		},
	),
}

def	PRE_SAVE(data):		# K_T_F_POST_FORM
	'''
	after validation and cleaned data - but pre PRINT/SAVE/UPDATE
	seat_srf: object => int
	@param data:dict - ...
	@return - nothing
	'''
	data['seat_srf'] = data['seat_srf'].pk
	data['h_srf'] = data['h_srf'].pk

def	POST_LOAD(data):	# K_T_F_POST_LOAD
	data['seat_srf'] = SSRF.objects.get(pk = data['seat_srf'])
	data['h_srf'] = SSRF.objects.get(pk = data['h_srf'])

def	PRE_FORM(data):
	PRE_SAVE(data)

def	PRE_PRINT(data):
	'''
	Caps all text fields
	'''
	for i in data:
		v = data[i]
		if isinstance(v, unicode):
			data[i] = v.upper()
