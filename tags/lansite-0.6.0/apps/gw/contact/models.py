# -*- coding: utf-8 -*-

'''
lansite.gw.task.models.py

Multitask: subtasks w/o subj, desk, etc - just assignee, state
'''

from django.db import models

from gw.bits.models import *

class	Contact(Object):
	addr		= models.ManyToManyField(Address,	through='ContactAddr', verbose_name=u'Адреса')
	phone		= models.ManyToManyField(Phone,		through='ContactPhone', verbose_name=u'Телефоны')
	www		= models.ManyToManyField(WWW,		through='ContactWWW', verbose_name=u'WWW')
	email		= models.ManyToManyField(Email,		through='ContactEmail', verbose_name=u'Email')
	im		= models.ManyToManyField(IM,		through='ContactIM', verbose_name=u'IM')

#	def	__unicode__(self):
#		return self.name
	def	__unicode__(self):
		return u'Contact...'

	def	gettype(self):
		return u'Contact'

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Контакт'
		verbose_name_plural	= u'Контакты'

class	ContactAddrType(models.Model):
	'''
	Тип адреса: Юридический, Фактический
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('name', )
		verbose_name		= u'Тип адреса контакта'
		verbose_name_plural	= u'Типы адресов контактов'

class	ContactAddr(models.Model):
	contact		= models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
	addr		= models.ForeignKey(Address, null=False, blank=False, verbose_name=u'Адрес')
	types		= models.ManyToManyField(ContactAddrType, through='Contact2AddrType', verbose_name=u'Типы')

	def	asstr(self):
		return u'%s: %s (%s)' % (self.contact, self.addr, self.type)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Контакт.Адрес'
		ordering		= ('contact', 'addr',)
		unique_together		= (('contact', 'addr',),)
		verbose_name_plural	= u'Контакты.Адреса'

class	Contact2AddrType(models.Model):
	type		= models.ForeignKey(ContactAddrType, null=False, blank=False, verbose_name=u'Тип')
	caddr		= models.ForeignKey(ContactAddr, null=False, blank=False, verbose_name=u'Контакт.Адрес')

	def	asstr(self):
		return u'%s: %s' % (self.phone, self.type)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Тип адреса контакта'
		verbose_name_plural	= u'Типы адресов контактов'
		ordering		= ('caddr', 'type',)
		unique_together		= (('type', 'caddr',),)

class	ContactPhone(models.Model):
	contact		= models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
	phone		= models.ForeignKey(Phone, null=False, blank=False, verbose_name=u'Телефон')
	ext		= models.CharField(max_length=4, null=True, blank=True, verbose_name=u'DTMF')

	def	__unicode__(self):
		return u'%s: %s (%s)' % (self.contact, self.phone, self.ext)

	class	Meta:
		app_label = 'gw'
		ordering		= ('contact', 'phone',)
		unique_together		= (('contact', 'phone',),)
		verbose_name		= u'Контакт.Телефон'
		verbose_name_plural	= u'Контакты.Телефоны'

class	ContactWWW(models.Model):
	'''
	TODO: URL => www
	'''
	contact		= models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
	www		= models.ForeignKey(WWW, null=False, blank=False, verbose_name=u'WWW')

	def	asstr(self):
		return u'%s: %s' % (self.contact, self.www)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('contact', 'www',)
		unique_together		= (('contact', 'www',),)
		verbose_name		= u'Контакт.WWW'
		verbose_name_plural	= u'Контакты.WWW'

class	ContactEmail(models.Model):
	contact		= models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
	email		= models.ForeignKey(Email, null=False, blank=False, verbose_name=u'Email')

	def	asstr(self):
		return u'%s: %s' % (self.contact, self.email)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('contact', 'email',)
		unique_together		= (('contact', 'email',),)
		verbose_name		= u'Контакт.Email'
		verbose_name_plural	= u'Контакты.Email'

class	ContactIM(models.Model):
	contact		= models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
	im		= models.ForeignKey(IM, null=False, blank=False, verbose_name=u'IM')

	def	asstr(self):
		return u'%s: %s: %s' % (self.contact, self.im.account, self.im.type)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('contact', 'im',)
		unique_together		= (('contact', 'im',),)
		verbose_name		= u'Контакт.IM'
		verbose_name_plural	= u'Контакты.IM'

class	Person(Contact):
	firstname	= models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Имя')
	midname		= models.CharField(max_length=24, null=True, blank=True, verbose_name=u'Отчество')
	lastname	= models.CharField(max_length=24, null=True, blank=True, verbose_name=u'Фамилия')
	birthdate	= models.DateField(null=True, blank=True, verbose_name=u'День рождения')
	sex		= models.BooleanField(null=False, blank=False, default=True, verbose_name=u'Пол')

	def	__unicode__(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

	def	gettype(self):
		return u'Person'

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Человек'
		verbose_name_plural	= u'Люди'

class	Org(Contact):
	cn		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Наименование')
	shortname	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Полное наименование')
	brandname	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Фирменное наименование')
	egruldate	= models.DateField(null=True, blank=True, verbose_name=u'Дата регистрации в ЕГРЮЛ')
	inn		= models.CharField(null=True, blank=True, max_length=12, unique=True, verbose_name=u'ИНН')
	kpp		= models.CharField(null=True, blank=True, max_length= 9, verbose_name=u'КПП')
	ogrn		= models.CharField(null=True, blank=True, max_length=15, unique=True, verbose_name=u'ОГРН')
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')

	def	__unicode__(self):
		return self.cn


	def	gettype(self):
		return u'Org'

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Организация'
		verbose_name_plural = u'Организации'

class	JobRole(models.Model):
	name		= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

	def	asstr(self):
		retvalue = self.name
		if self.comments:
			retvalue += u' (%s)' % self.comments
		return retvalue

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering = ('name',)
		verbose_name = u'Должность'
		verbose_name_plural = u'Должности'

class	OrgStuff(models.Model):
	'''
	TODO: rename to Stuff
	'''
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	role		= models.ForeignKey(JobRole, verbose_name=u'Должность')
	person		= models.ForeignKey(Person, verbose_name=u'Человек')

	def	__unicode__(self):
		return u'%s, %s: %s' % (self.org, self.role, self.person)

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Организация.Должностное лицо'
		verbose_name_plural	= u'Организация.Должностные лица'
		unique_together		= [('org', 'role', 'person')]
