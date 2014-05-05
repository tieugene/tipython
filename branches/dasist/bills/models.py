# -*- coding: utf-8 -*-

# 1. django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

# 2. 3rd parties

# 3. system
import os, sys, datetime
from StringIO import StringIO

# 4. local
#print sys.path
from core.models import File, FileSeq
#import core

#state_id = {	# rpoint==None, done
#	(True,	None):	1,		# Draft
#	(False,	None ):	2,		# OnWay
#	(True,	True ):	3,		# Accepted
#	(True,	False):	4,		# Rejected
#}

state_id = {	# rpoint==None, done
	(True,	None):	1,		# Draft
	(False,	None ):	2,		# OnWay
	(False,	True):	3,		# OnPay
	(True,	True):	4,		# Accepted
	(True,	False):	5,		# Rejected
	(False,	False):	6,		# <impossible>
}

state_name = {	# rpoint==None, done
	(True,	None):	'Черновик',	# Draft
	(False,	None ):	'В пути',	# OnWay
	(False,	True):	'В оплате',	# OnPay
	(True,	True ):	'Исполнен',	# Accepted
	(True,	False):	'Завернут',	# Rejected
}

state_color = {	# rpoint==None, done	http://www.w3schools.com/html/html_colornames.asp
	(True,	None):	'white',	# Draft
	(False,	None ):	'FFFF99',	# OnWay (yellow)
	(False,	True):	'aqua',		# OnPay
	(True,	True ):	'chartreuse',	# Accepted (green)
	(True,	False):	'silver',	# Rejected (gray)
}

# Refs
class	Role(models.Model):
	'''
	Predefined roles
	TODO: m2m user [via Approver]
	'''
	id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	name	= models.CharField(max_length=32, verbose_name=u'Наименование')
	#users		= models.ManyToManyField(User, null=True, blank=True, related_name='history', through='Approver', verbose_name=u'Подписанты')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Роль'
		verbose_name_plural     = u'Роли'

class	Approver(models.Model):
	'''
	'''
	user	= models.OneToOneField(User, primary_key=True, verbose_name=u'Пользователь')
	role	= models.ForeignKey(Role, verbose_name=u'Роль')
	jobtit	= models.CharField(max_length=32, verbose_name=u'Должность')
	canadd	= models.BooleanField(verbose_name=u'Может создавать')

	class   Meta:
		ordering                = ('role', )
		verbose_name            = u'Подписант'
		verbose_name_plural     = u'Подписанты'

	def	get_fio(self):
		io = self.user.first_name.split()
		return '%s %s. %s.' % (self.user.last_name, io[0][0], io[1][0])

	def	__unicode__(self):
		return '%s %s (%s, %s)' % (self.user.last_name, self.user.first_name, self.jobtit, self.role.name)

class	Place(models.Model):
	#id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	name	= models.CharField(max_length=32, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Объект'
		verbose_name_plural     = u'Объекты'

class	Subject(models.Model):
	#id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	place	= models.ForeignKey(Place, related_name='subjects', verbose_name=u'Объект')
	name	= models.CharField(max_length=32, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('place', 'name',),)
		ordering                = ('place', 'id', )
		verbose_name            = u'ПодОбъект'
		verbose_name_plural     = u'ПодОбъект'

class	Department(models.Model):
	id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	name	= models.CharField(max_length=32, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Направление'
		verbose_name_plural     = u'Направления'

class	Payer(models.Model):
	id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	name	= models.CharField(max_length=32, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Плательщик'
		verbose_name_plural     = u'Плательщики'

'''
class	RouteTemplate(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
	name		= models.CharField(max_length=32, verbose_name=u'Наименование')
	approvers	= models.ManyToManyField(Approver, null=True, blank=True, related_name='acl', through='RouteTemplateACL', verbose_name=u'Подписанты')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name'),)
		ordering                = ('id',)
		verbose_name            = u'Шаблон маршрута'
		verbose_name_plural     = u'Шаблоны маршрутов'

class	RouteTemplateItem(models.Model):
	tpl	= models.ForeignKey(RouteTemplate, verbose_name=u'Шаблон маршрута')
	order	= models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'#')
	role	= models.ForeignKey(Role, verbose_name=u'Роль')
	approve	= models.ForeignKey(Approver, null=True, blank=True, verbose_name=u'Подписант')
	areq	= models.BooleanField(verbose_name=u'Требует Подписанта')

	def	__unicode__(self):
		return '$s #%d' % (self.tpl, self.order)

	class   Meta:
		unique_together		= (('tpl', 'order'),)
		ordering                = ('tpl', 'order')
		verbose_name            = u'Точка шаблона маршрута'
		verbose_name_plural     = u'Точки шаблонов маршрутов'

class	RouteTemplateACL(models.Model):
	tpl	= models.ForeignKey(RouteTemplate, verbose_name=u'Шаблон маршрута')
	approve	= models.ForeignKey(Approver, verbose_name=u'Подписант')

	class   Meta:
		unique_together		= (('tpl', 'approve'),)
		ordering                = ('pk',)
		verbose_name            = u'Права на маршрут'
		verbose_name_plural     = u'Права на маршруты'
'''

# Working
class	Bill(models.Model):
	'''
	'''
	fileseq		= models.OneToOneField(FileSeq, primary_key=True, verbose_name=u'Файлы')
	place		= models.ForeignKey(Place, null=False, blank=False, verbose_name=u'Объект')
	subject		= models.ForeignKey(Subject, null=True, blank=True, verbose_name=u'ПодОбъект')
	depart		= models.ForeignKey(Department, null=True, blank=True, verbose_name=u'Направление')
	payer		= models.ForeignKey(Payer, null=True, blank=True, verbose_name=u'Плательщик')
	supplier	= models.CharField(max_length=64, verbose_name=u'Поставщик')
	billno		= models.CharField(max_length=64, verbose_name=u'Номер счета')
	billdate	= models.DateField(verbose_name=u'Дата счета')
	billsum		= models.PositiveIntegerField(default=0, verbose_name=u'Сумма счета')
	payedsum	= models.PositiveIntegerField(default=0, verbose_name=u'Оплачено')
	topaysum	= models.PositiveIntegerField(default=0, verbose_name=u'Сумма к оплате')
	assign		= models.ForeignKey(Approver, related_name='assigned', verbose_name=u'Исполнитель')
	rpoint		= models.ForeignKey('Route', null=True, blank=True, related_name='rbill', verbose_name=u'Точка маршрута')
	done		= models.NullBooleanField(null=True, blank=True, verbose_name=u'Закрыт')
	#route		= SortedManyToManyField(Approver, null=True, blank=True, related_name='route', verbose_name=u'Маршрут')
	#history		= models.ManyToManyField(Approver, null=True, blank=True, related_name='history', through='BillEvent', verbose_name=u'История')

	def     __unicode__(self):
		return str(self.pk)

	def	__get_state(self):
		return (self.rpoint==None, self.done)

	def	get_state_id(self):
		return state_id[self.__get_state()]

	def	get_state_name(self):
		return state_name[self.__get_state()]

	def	get_state_color(self):
		return state_color[self.__get_state()]

	class   Meta:
		#unique_together		= (('scan', 'type', 'name'),)
		#ordering                = ('id',)
		verbose_name            = u'Счет'
		verbose_name_plural     = u'Счета'

class	Route(models.Model):
	bill	= models.ForeignKey(Bill, verbose_name=u'Счет')
	order	= models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'#')
	role	= models.ForeignKey(Role, verbose_name=u'Роль')
	approve	= models.ForeignKey(Approver, null=True, blank=True, verbose_name=u'Подписант')
	#state	= models.ForeignKey(State, verbose_name=u'Состояние')
	#action	= models.CharField(max_length=16, verbose_name=u'Действие')

	def	__unicode__(self):
		return '%d.%d: %s' % (self.bill.pk, self.order, self.approve.get_fio() if self.approve else self.role.name)

	def	get_str(self):
		return self.approve.get_fio() if self.approve else self.role.name

	class   Meta:
		unique_together		= (('bill', 'order',),)
		ordering                = ('bill', 'order',)
		verbose_name            = u'Точка маршрута'
		verbose_name_plural     = u'Точки маршрута'

class	Event(models.Model):
	bill	= models.ForeignKey(Bill, related_name='events', verbose_name=u'Счет')
	approve	= models.ForeignKey(Approver, verbose_name=u'Подписант')
	resume	= models.BooleanField(verbose_name=u'Резолюция')
	ctime	= models.DateTimeField(auto_now_add=True, verbose_name=u'ДатаВремя')
	comment	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Камменты')

	def	__unicode__(self):
		return '%s: %s' % (self.approve, self.comment)

	class   Meta:
		ordering                = ('ctime',)
		verbose_name            = u'Резолюция'
		verbose_name_plural     = u'Резолюции'
