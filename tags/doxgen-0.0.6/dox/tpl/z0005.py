# -*- coding: utf-8 -*-
'''
'''
from django.utils.datastructures import SortedDict
# 3. system
import sys, datetime

from consts import *

reload(sys)
sys.setdefaultencoding('utf-8')

list_sex = [
	(1, 'мужской'),
	(2, 'женский'),
]
list_visa = [
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

DATA = {
	K_T_UUID:	'D886C413BCFF40CE8F7833A57673F3CF',
	K_T_NAME:	'Уведомление мигранта',
	K_T_COMMENTS:	'Уведомление о прибытии иностранного гражданина или лица без гражданства в место пребывания',
	K_T_FIELD:	SortedDict([
		('m_lastname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Фамилия',
					'max_length':	35,
				}
		}),
		('m_firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Имя, Отчество',
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
					'label':	'Мигрант. Дата рождения',
				}
		}),
		('m_sex', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'пол',
					'choices':	list_sex,
				}
		}),
		('m_birthcountry', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Государство рождения',
					'max_length':	33,
				}
		}),
		('m_birthlocation', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Город рождения',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('m_idcard_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Документ.Вид',
					'help_text':	'удостоверяющий личность',
					'max_length':	11,
				}
		}),
		('m_idcard_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Документ.Серия',
					'max_length':	4,
				}
		}),
		('m_idcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Документ.Номер',
					'max_length':	9,
				}
		}),
		('m_idcard_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Документ.Выдан',
				}
		}),
		('m_idcard_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Документ.До',
				}
		}),
		('m_visa_type', {
				K_T_FIELD_T:	K_CHOICE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Виза.Вид',
					'help_text':	'документ, подтверждающий право на пребывание (проживание) в РФ',
					'choices':	list_visa,
					'required':	False,
				}
		}),
		('m_visa_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Виза.Серия',
					'max_length':	4,
				}
		}),
		('m_visa_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Виза.Номер',
					'max_length':	9,
				}
		}),
		('m_visa_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Виза.Выдан',
				}
		}),
		('m_visa_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Мигрант. Виза.До',
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
					'label':	'Миграционная карта.Серия',
					'max_length':	4,
				}
		}),
		('mcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Миграционная карта.Номер',
					'max_length':	7,
				}
		}),
		('represent', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Сведения о законных представителях',
					'max_length':	95,
				}
		}),
		('seat_srf', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. СРФ',
					'help_text':	'область, край, республика, АО',
					'max_length':	33,
				}
		}),
		('seat_region', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Район',
					'max_length':	35,
					'required':	False,
				}
		}),
		('seat_city', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Город',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('seat_street', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Улица',
					'max_length':	35,
				}
		}),
		('seat_house', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Дом',
					'max_length':	4,
				}
		}),
		('seat_housing', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Корпус',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_building', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Строение',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_flat', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Квартира',
					'max_length':	4,
					'required':	False,
				}
		}),
		('seat_phone', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Место пребывания. Телефон',
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
					'label':	'Хозяин. Фамилия',
					'max_length':	35,
				}
		}),
		('h_firstname', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Имя, Отчество',
					'max_length':	35,
				}
		}),
		('h_idcard_type', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Документ.Вид',
					'help_text':	'удостоверяющий личность',
					'max_length':	11,
				}
		}),
		('h_idcard_sn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Документ.Серия',
					'max_length':	4,
				}
		}),
		('h_idcard_no', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Документ.Номер',
					'max_length':	9,
				}
		}),
		('h_idcard_date', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Документ.Выдан',
				}
		}),
		('h_idcard_expired', {
				K_T_FIELD_T:	K_DATE_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Документ.До',
				}
		}),
		('h_srf', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. СРФ',
					'help_text':	'область, край, республика, АО',
					'max_length':	33,
				}
		}),
		('h_region', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Район',
					'max_length':	35,
					'required':	False,
				}
		}),
		('h_city', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Город',
					'help_text':	'или другой населенный пункт',
					'max_length':	33,
				}
		}),
		('h_street', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Улица',
					'max_length':	35,
				}
		}),
		('h_house', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Дом',
					'max_length':	4,
				}
		}),
		('h_housing', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Корпус',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_building', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Строение',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_flat', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Квартира',
					'max_length':	4,
					'required':	False,
				}
		}),
		('h_phone', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Хозяин. Телефон',
					'max_length':	10,
					'required':	False,
				}
		}),
		('org_name', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Организация. Наименование',
					'max_length':	52,
					'required':	False,
				}
		}),
		('org_addr', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Организация. Факт. адрес',
					'max_length':	52,
					'required':	False,
				}
		}),
		('org_inn', {
				K_T_FIELD_T:	K_CHAR_FIELD,
				K_T_FIELD_A:	{
					'label':	'Организация. ИНН',
					'min_length':	12,
					'max_length':	12,
					'required':	False,
				}
		}),
	]),
	K_T_T:	{
		K_T_T_PRINT:	'print/z0005.rml',
	}
}
