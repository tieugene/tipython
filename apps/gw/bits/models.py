# -*- coding: utf-8 -*-

'''
lansite.gw.bits.models.py
'''

from django.db import models
from django.contrib.auth.models import User
from polymorphic import PolymorphicModel
from treebeard.al_tree import AL_Node

import bigint

from ref.models import Kladr

class	GwUser(models.Model):
	user		= models.OneToOneField(User, primary_key=True, verbose_name=u'Пользователь')

	def	__unicode__(self):
		return self.user.username

	class	Meta:
		app_label = 'gw'
		ordering = ('user',)
		verbose_name = u'Пользователь GW'
		verbose_name_plural = u'Пользователи GW'

class	USManager(models.Manager):
	'''
	UserSetting manager
	'''
	def	cu_ufa(self, user, form, action, object, value):
		'''
		Create or update object/value/ for given user/form/action
		Used for sort set
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		@param o:str - string
		@param v:str - string
		'''
		q = self.filter(user=user, form=form, action=action)
		if (q):
			r = q[0]
			if ((r.object != object) or (r.value != value)):
				r.object = object
				r.value = value
				r.save()
		else:
			UserSetting(user=user, form=form, action=action, object=object, value=value).save()

	def	cu_ufao(self, user, form, action, object, value):
		'''
		Create or update object/value/ for given user/form/action
		Used for filter set
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		@param o:str - string
		@param v:str - string
		'''
		q = self.filter(user=user, form=form, action=action, object=object)
		if (q):
			r = q[0]
			if (r.value != value):
				r.value = value
				r.save()
		else:
			UserSetting(user=user, form=form, action=action, object=object, value=value).save()

	def	del_ufao(self, user, form, action, object = None):
		'''
		Delete all of given user/form/actions
		Used for delete sort|filters
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		'''
		if (o == None):
			self.filter(user=user, form=form, action=action).delete()
		else:
			self.filter(user=user, form=form, action=action, object=object).delete()

	def	get_sort(self, user, form):
		'''
		@return (order:str, name:str, value:int)
		'''
		retvalue = (None, None, None)
		sort = self.filter(user=user, form=form, action='sort')
		if sort:
			o = sort[0].object
			v = int(sort[0].value)	# 1/-1
			print sort[0].value
			if (v == 1):
				retvalue = (o, v, '-' + o)
			else:
				retvalue = (o, v, o)
		return retvalue

class	UserSetting(models.Model):
	user		= models.ForeignKey(User, blank=False, null=False, verbose_name=u'Пользователь')
	form		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Форма')
	action		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Действие')
	object		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Объект')
	value		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Значение')
	objects		= USManager()

	def	__unicode__(self):
		return u'%s.%s.%s.%s.%s' % (self.user.username, self.form, self.object, self.action, self.value )

	class	Meta:
		app_label = 'gw'
		ordering = ('user', 'form', 'object', 'action')
		verbose_name = u'Настройки пользователя'
		verbose_name_plural = u'Настройки пользователей'

class	Object(PolymorphicModel):
	'''
	Объект - прародитель всех остальных.
	'''
	'''
	child	= models.ManyToManyField('self', symmetrical=False, through='SubObject', verbose_name=u'Объекты')
	'''

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Объект'
		verbose_name_plural	= u'Объекты'

'''
class	SubObject(models.Model):
	master		= models.ForeignKey(Object, related_name='slave', verbose_name=u'Хозяин')
	slave		= models.OneToOneField(Object, related_name='master', primary_key=True, verbose_name=u'Объект')

	class	Meta:
		verbose_name		= u'Подобъект'
		verbose_name_plural	= u'Подобъекты'
'''

class	AddrShort(models.Model):
	'''
	Сокращение для адреса: ул.=улица etc
	'''
	name		= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Полное наименование')

	def	__unicode__(self):
		return u'%s (%s)' % (self.name, self.fullname)

	class	Meta:
		app_label = 'gw'
		ordering		= ('name', )
		verbose_name		= u'Сокращение адреса'
		verbose_name_plural	= u'Сокращения адресов'

class	AddrType(models.Model):
	'''
	Тип адреса: Домашний, Юридический, Почтовый, Доставки etc
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	abbr		= models.CharField(max_length=6, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	name		= models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип адреса'
		verbose_name_plural	= u'Типы адресов'

class	Address(Object, AL_Node):
	'''
	Адрес (РФ) - рекурсивный
	'''
	name		= models.CharField(max_length=60, null=False, blank=False, verbose_name=u'Наименование')
	type		= models.ForeignKey(AddrShort, null=True, blank=True, verbose_name=u'Сокращение')
	typeplace	= models.SmallIntegerField(null=True, blank=True, verbose_name=u'Расположение сокращения')	# type пишется слева, справа, в середине
	parent		= models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Предок')
	publish		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Печатать')
	endpoint	= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Конец')
	zip		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Индекс')
	fullname	= models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Полный адрес')
	node_order_by	= ['name']

	def	__unicode__(self):
		return self.name

	def	asfullstr(self):
		retvalue = u''
		for i in self.getparents():
			retvalue = retvalue + i.name + ', '
		return retvalue + self.name

	def	mkfullname(self):
		'''
		Build full name recursively
		'''
		if self.endpoint:
			tmp = list()
			for i in self.get_ancestors():
				if i.publish:
					if i.type:
						tmp.append(i.type.name + u'. ' + i.name)
					else:
						tmp.append(i.name)
			if self.publish:
				if self.type:
					tmp.append(self.type.name + u'. ' + self.name)
				else:
					tmp.append(self.name)
			self.fullname = ', '.join(tmp)
		else:
			self.fullname = self.name

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Адрес'
		verbose_name_plural	= u'Адреса'
		ordering		= ('name',)

class	AddrKladr(models.Model):
	address		= models.OneToOneField(Address, verbose_name=u'Адрес')
	kladr		= bigint.BigForeignKey(Kladr, null=False, blank=False, db_index=True, verbose_name=u'КЛАДР')

	def	__unicode__(self):
		return self.address

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Адрес.Кладр'
		verbose_name_plural	= u'Адреса.Кладр'

class	PhoneType(models.Model):
	'''
	Тип телефона
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	abbr		= models.CharField(max_length=5, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	name		= models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип телефона'
		verbose_name_plural	= u'Типы телефонов'

class	Phone(Object):
	'''
	Телефонный номер.
	'''
	no		= models.CharField(max_length=15, null=False, blank=False, unique=True, verbose_name=u'Номер')
	types		= models.ManyToManyField(PhoneType, through='Phone2Type', verbose_name=u'Типы')

	def	__unicode__(self):
		return self.no

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Телефон'
		verbose_name_plural	= u'Телефоны'
		ordering		= ('no',)

class	Phone2Type(models.Model):
	type		= models.ForeignKey(PhoneType, null=False, blank=False, verbose_name=u'Тип')
	phone		= models.ForeignKey(Phone, null=False, blank=False, verbose_name=u'Телефон')

	def	asstr(self):
		return u'%s: %s' % (self.phone, self.type)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Телефон.Тип'
		verbose_name_plural	= u'Телефон.Типы'
		ordering		= ('phone', 'type',)
		unique_together		= (('type', 'phone',),)

class	__URL(Object):
	URL		= models.URLField(unique=True, verbose_name=u'URL')

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('URL',)
		abstract		= True

class	WWW(Object):
	'''
	Web-ресурс.
	'''
	URL		= models.URLField(unique=True, verbose_name=u'URL')

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'WWW'
		verbose_name_plural	= u'WWW'
		ordering		= ('URL',)

class	Email(Object):
	'''
	E-mail
	'''
	URL		= models.EmailField(unique=True, verbose_name=u'Email')

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'E-mail'
		verbose_name_plural	= u'E-mail'
		ordering		= ('URL',)

class	IMType(models.Model):
	'''
	Тип IM
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	comments	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Комментарии')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип IM'
		verbose_name_plural	= u'Типы IM'

class	IM(Object):
	account		= models.CharField(max_length=64, null=False, blank=False, verbose_name=u'Учетная запись')
	type		= models.ForeignKey(IMType, null=False, blank=False, verbose_name=u'Тип')

	def	asstr(self):
		return u'%s: %s' % (self.type.name, self.account)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'IM'
		verbose_name_plural	= u'IM'
		ordering		= ('type', 'account',)
		unique_together		= (('account', 'type',),)
