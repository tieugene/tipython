# -*- coding: utf-8 -*-

# 1. django
from django.db import models
from django.contrib.auth.models import User

# 3. system
import datetime

class	ScanFile(models.Model):
	'''
	TODO: cache
	'''
	mime	= models.CharField(max_length=64, verbose_name=u'MIME')
	name    = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Наименование')

class	Bill(models.Model):
	'''
	Fields:
	[Assigne]
	[Approver]
	?desc:txt
	?ctime:datetime - время создания
	?etime:datetime - время окончания
	??Поставщик
	??Номер счета
	??Дата счета
	??Сумма счета
	'''
	scan	= models.OneToOneField(ScanFile, primary_key=True, verbose_name=u'Скан')
	project	= models.CharField(max_length=64, verbose_name=u'Объект')
	depart	= models.CharField(max_length=64, verbose_name=u'Направление')
	assign	= models.ForeignKey(User, related_name='assigned', verbose_name=u'Исполнитель')
	approve	= models.ForeignKey(User, related_name='inbox',    verbose_name=u'Согласующий')
	isalive	= models.BooleanField(verbose_name=u'Живой')
	isgood	= models.BooleanField(verbose_name=u'Хороший')
	#created	= models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')	# editable-False
	#updated	= models.DateTimeField(auto_now=True, verbose_name=u'Изменен')		# editable-False
	#data	= models.TextField(verbose_name=u'Данные')

	def     __unicode__(self):
		return self.name

	class   Meta:
		#unique_together		= (('scan', 'type', 'name'),)
		#ordering                = ('id',)
		verbose_name            = u'Счет'
		verbose_name_plural     = u'Счета'

class	BillRoute(models.Model):
	bill	= models.ForeignKey(Bill, related_name='route', verbose_name=u'Счет')
	orderno	= models.PositiveSmallIntegerField(verbose_name=u'#')
	user	= models.ForeignKey(User, verbose_name=u'Пользователь')

	def	__unicode__(self):
		return self.user

	class   Meta:
		ordering                = ('orderno',)
		verbose_name            = u'ТочкаМаршрута'
		verbose_name_plural     = u'ТочкиМаршрута'

class	BillEvent(models.Model):
	bill	= models.ForeignKey(Bill, related_name='history', verbose_name=u'Счет')
	user	= models.ForeignKey(User, verbose_name=u'Пользователь')
	ctime	= models.DateTimeField(auto_now_add=True, verbose_name=u'ДатаВремя')
	comment	= models.TextField(verbose_name=u'Камменты')

	def	__unicode__(self):
		return self.user

	class   Meta:
		ordering                = ('ctime',)
		verbose_name            = u'Событие'
		verbose_name_plural     = u'События'

class	Role(models.Model):
	id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'ID')
	name	= models.CharField(max_length=16, verbose_name=u'Наименование')

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Роль'
		verbose_name_plural     = u'Роли'

class	Approver(models.Model):
	user	= models.OneToOneField(User, primary_key=True, verbose_name=u'Юзверь')
	role	= models.ForeignKey(Role, verbose_name=u'Роль')

	class   Meta:
		unique_together		= (('user', 'role',),)
		ordering                = ('user', )
		verbose_name            = u'РольПользователя'
		verbose_name_plural     = u'РолиПользователей'
