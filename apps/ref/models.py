# -*- coding: utf-8 -*-
'''
Okv	ОКВ	=> ISO 4217
Oksm	ОКСМ	=> ISO 3166
BIK	БИК	=> ISO 9362
'''

import os

from django.db import models
from treebeard.al_tree import AL_Node

import bigint

# = ОКАТО =

class	Okato(AL_Node):
	'''
	Общероссийский классификатор объектов административно-территориального деления
	id - by OKATO
	http://www.fomsrt.ru/nsi/handbooks/index.php ?ELEMENT_ID=437
	'''
	id		= bigint.BigIntegerField(primary_key=True, verbose_name=u'ID')
	parent		= bigint.BigForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Группа')
	code		= models.CharField(max_length=11, unique=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, null=False, blank=False, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Доп. информация')
	node_order_by	= ['id']

	def	asstr(self):
		return u'%s: %s' % (self.code, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКАТО'
		verbose_name_plural = u'ОКАТО'

# = ОКОПФ =

class	Okopf(AL_Node):
	'''
	id - by OKOPF, short int
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	parent		= models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Группа')
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	shortname	= models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Краткое наименование')
	disabled	= models.BooleanField(blank=False, default=False, verbose_name=u'Не выбирать')
	node_order_by	= ['id']

	def	__unicode__(self):
		return self.name

	@models.permalink
	def	get_absolute_url(self):
		return('okopf_view', [str(self.id)])

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКОПФ'
		verbose_name_plural = u'ОКОПФ'

# = ОКСМ =

class	Oksm(models.Model):
	'''
	id - by OKSM
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	alpha2		= models.CharField(max_length=2, unique=True, verbose_name=u'Альфа-2')
	alpha3		= models.CharField(max_length=3, unique=True, verbose_name=u'Альфа-2')
	name		= models.CharField(max_length=100, unique=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Полное наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'ОКСМ'
		verbose_name_plural = u'ОКСМ'

# = ОКВЭД =

class	Okved(models.Model):
	'''
	id - by OKVED, str
	'''
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	code		= models.CharField(max_length=6, unique=True, verbose_name=u'Код')
	name		= models.CharField(max_length=400, blank=False, unique=False, verbose_name=u'Наименование')

	def	asstr(self):
		return u'%s: %s' % (self.code, self.name[:100])

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКВЭД'
		verbose_name_plural = u'ОКВЭД'

# = Phones =

class	PhoneCountry(models.Model):
	'''
	Телефонный код страны/глобальной службы
	'''
	no		= models.CharField(max_length=3, unique=True, verbose_name=u'Код')

	def	asstr(self):
		return self.no

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Телефон.Страна'
		verbose_name_plural	= u'Телефон.Страны'

class	PhoneTrunk(models.Model):
	'''
	Телефонный код направления
	'''
	country		= models.ForeignKey(PhoneCountry, null=False, blank=False, verbose_name=u'Страна')
	trunk		= models.CharField(max_length=13, null=False, blank=False, verbose_name=u'Магистраль')

	def	asstr(self):
		return self.id

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Телефон.Страна.Направление'
		verbose_name_plural	= u'Телефон.Страна.Направления'
		unique_together		= (('country', 'trunk'),)

# = KLADR =

class	KladrShort(models.Model):	# SOCRBASE
	'''
	Сокращения.
	'''
	name		= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Наименование')		# SCNAME
	fullname	= models.CharField(max_length=29, blank=False, unique=True, verbose_name=u'Полное наименование')	# SOCRNAME

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'КЛАДР.Сокращение'
		verbose_name_plural	= u'КЛАДР.Сокращения'

class	KladrStateType(models.Model):
	'''
	Статусы - ...?
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	comments	= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Каменты')

	def	asstr(self):
		return self.id

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'КЛАДР.Статус'
		verbose_name_plural	= u'КЛАДР.Статусы'

class	Kladr(AL_Node):
	'''
	Сам КЛАДР (KLADR+STREET)
	'''
	id		= bigint.BigIntegerField(primary_key=True, verbose_name=u'Код')						# CODE
	parent		= bigint.BigForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Группа')
	name		= models.CharField(max_length=40, null=False, blank=False, unique=False, verbose_name=u'Наименование')	# NAME
	short		= models.ForeignKey(KladrShort, null=True, blank=True, verbose_name=u'Сокращение')			# SOCR
	zip		= models.CharField(max_length=6, null=True, blank=True, unique=False, verbose_name=u'Индекс')		# INDEX
	center		= models.ForeignKey(KladrStateType, null=True, blank=True, unique=False, verbose_name=u'Центр')		# STATUS
	node_order_by	= ['id']

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'КЛАДР'
		verbose_name_plural	= u'КЛАДР'

class	KladrOkato(models.Model):
	kladr		= models.OneToOneField(Kladr, primary_key=True, verbose_name=u'КЛАДР')
	okato		= bigint.BigIntegerField(null=False, blank=False, db_index=True, verbose_name=u'ОКАТО')

# = БИК =
