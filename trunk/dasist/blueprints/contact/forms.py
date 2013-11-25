# -*- coding: UTF-8 -*-
__author__ = 'ti.eugene@gmail.com'

from models import Contact

#from flask_wtf import Form
from flask.ext.wtf import Form
#from wtforms.ext.sqlalchemy.orm import model_form, QuerySelectField, QuerySelectMultipleField
import wtforms as wtf
from wtforms.validators import Required, EqualTo, Email
from wtforms import validators
from datetime import datetime
# from wtforms.fields.html5 import DateField

#ContactForm = model_form(Contact, base_class=Form)

class AddressForm(Form):
	addr = wtf.StringField(u'Адрес',validators=[validators.Length(max=254)])

	def __init__(self, csrf_enabled=False, *args, **kwargs):
		super(FilterForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

class ContactForm(Form):
	lastname = wtf.StringField(u'Фамилия',validators=[validators.Length(max=64)])
	firstname = wtf.StringField(u'Имя',validators=[Required(),validators.Length(max=64)])
	midname = wtf.StringField(u'Отчество',validators=[validators.Length(max=64)])
	birthdate = wtf.DateField(u'Дата рождения')
	addresses = wtf.FieldList(wtf.FormField(AddressForm))
