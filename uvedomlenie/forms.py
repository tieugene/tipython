# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, DateField, SelectField
from wtforms.validators import Required, Length, Optional

gender_list = [
	('1', 'Мужской'),
	('2', 'Женский'),
]
aim_list = [
	('1', 'Служебная'),
	('2', 'Туризм'),
	('3', 'Деловая'),
	('4', 'Учеба'),
	('5', 'Работа'),
	('6', 'Частная'),
	('7', 'Транзит'),
	('8', 'Гуманитарная'),
	('9', 'Другая'),
]
perm_list = [
	('0', '---'),
	('1', 'Виза'),
	('2', 'ВНЖ'),
	('3', 'РВП'),
]
a_list = [
	('1', 'Организация'),
	('2', 'Физ. лицо'),
]

class MyForm(Form):
    ''' 55 полей, цукко, 22 mandatory string/date, 4 selects '''
    # 1. Сведения о лице, подлежащем постановке на учет по месту пребывания
    m_lastname      = StringField('Фамилия', validators = [Required(), Length(max=35)])
    m_firstname     = StringField('Имя, отчество', validators = [Required(), Length(max=35)])
    m_citizenship   = StringField('Гражданство', validators = [Required(), Length(max=34)])
    m_gender        = SelectField('Пол', choices=gender_list)
    m_aim           = SelectField('Цель въезда', choices=aim_list)
    m_profession    = StringField('Профессия', validators = [Length(max=23)])
    m_arrived       = DateField('Дата въезда', validators = [Required()], format='%d.%m.%Y')
    m_expired       = DateField('Пребывает до', validators = [Required()], format='%d.%m.%Y')
    m_agent         = StringField('Сведения о законных представителях', validators = [Length(max=38)])
    m_prev_addr     = StringField('Адрес прежнего места пребывания в РФ', validators = [Length(max=57)])
    # Дата и место рождения:
    m_birth_date    = DateField('Дата рождения', validators = [Required()], format='%d.%m.%Y')
    m_birth_country = StringField('Страна', validators = [Length(max=33)])
    m_birth_city    = StringField('Город или другой населенный пункт', validators = [Length(max=33)])
    # Удостоверение личности
    m_doc_type      = StringField('Вид', validators = [Required()])
    m_doc_series    = StringField('Серия', validators = [Length(max=4)])
    m_doc_no        = StringField('Номер', validators = [Required(), Length(max=9)])
    m_doc_date      = DateField('Дата выдачи', validators = [Required()], format='%d.%m.%Y')
    m_doc_expired   = DateField('Срок действия', validators = [Optional()], format='%d.%m.%Y')
    # Вид и реквизиты документы, подтверждающий право на пребывание (проживание) в Российской федерации:
    m_perm_type     = SelectField('Вид', choices=perm_list)
    m_perm_series   = StringField('Серия', validators = [Length(max=4)])
    m_perm_no       = StringField('Номер', validators = [Length(max=9)])
    m_perm_date     = DateField('Дата выдачи', validators = [Optional()], format='%d.%m.%Y')
    m_perm_expired  = DateField('Срок действия', validators = [Optional()], format='%d.%m.%Y')
    # Миграционная карта:
    m_mk_series     = StringField('Серия', validators = [Length(max=4)])
    m_mk_no         = StringField('Номер', validators = [Length(max=7)])
    # 2. Сведения о месте пребывания:
    addr_sf         = StringField('Область, край, республика, АО', validators = [Length(max=33)])
    addr_region     = StringField('Район', validators = [Length(max=35)])
    addr_city       = StringField('Город или другой населенный пункт', validators = [Required(), Length(max=33)])
    addr_street     = StringField('Улица', validators = [Required(), Length(max=35)])
    addr_house      = StringField('Дом', validators = [Required(), Length(max=4)])
    addr_housing    = StringField('Корпус', validators = [Length(max=4)])
    addr_building   = StringField('Строение', validators = [Length(max=4)])
    addr_app        = StringField('Квартира', validators = [Length(max=4)])
    addr_tel        = StringField('Телефон', validators = [Length(max=10)])    	# код и номер, подряд
    # 3. Сведения о принимающей стороне:
    a_type          = SelectField('Вид', choices=a_list)
    a_lastname      = StringField('Фамилия', validators = [Required(), Length(max=35)])
    a_firstname     = StringField('Имя, отчество', validators = [Required(), Length(max=35)])
    a_birth_date    = DateField('Дата рождения', validators = [Required()], format='%d.%m.%Y')
    # Удостоверение личности
    a_doc_type      = StringField('Вид', validators = [Required(), Length(max=11)])
    a_doc_series    = StringField('Серия', validators = [Required(), Length(max=4)])
    a_doc_no        = StringField('Номер', validators = [Required(), Length(max=9)])
    a_doc_date      = DateField('Дата выдачи', validators = [Required()], format='%d.%m.%Y')
    a_doc_expired   = DateField('Срок действия', validators = [Optional()], format='%d.%m.%Y')
    # Прописка
    a_addr_sf       = StringField('Область, край, республика, АО', validators = [Length(max=33)])
    a_addr_region   = StringField('Район', validators = [Length(max=35)])
    a_addr_city     = StringField('Город или другой населенный пункт', validators = [Required(), Length(max=33)])
    a_addr_street   = StringField('Улица', validators = [Required(), Length(max=35)])
    a_addr_house    = StringField('Дом', validators = [Required(), Length(max=4)])
    a_addr_housing  = StringField('Корпус', validators = [Length(max=4)])
    a_addr_building = StringField('Строение', validators = [Length(max=4)])
    a_addr_app      = StringField('Квартира', validators = [Length(max=4)])
    a_addr_tel      = StringField('Телефон', validators = [Length(max=10)])    	# код и номер, подряд
    # Организация
    a_org_name      = StringField('Наименование организации', validators = [Length(max=52)])
    a_org_addr      = StringField('Факт. адрес', validators = [Length(max=52)])
    a_org_inn       = StringField('ИНН', validators = [Length(max=12)])
