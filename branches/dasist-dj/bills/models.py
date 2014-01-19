# -*- coding: utf-8 -*-

# 1. django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# 2. 3rd parties
from sortedm2m.fields import SortedManyToManyField

# 3. system
import os, datetime

states = {	# isalive, isgood
	(True,  False): 1,	# Draft
	(True,  True ): 2,	# OnWay
	(False, True ): 3,	# Accepted
	(False, False): 4,	# Rejected
}

class	Role(models.Model):
	'''
	Predefined role model
	TODO: m2m user [via Approver]
	'''
	id	= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'ID')
	name	= models.CharField(max_length=16, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class   Meta:
		unique_together		= (('name',),)
		ordering                = ('id', )
		verbose_name            = u'Роль'
		verbose_name_plural     = u'Роли'

class	Approver(User):
	'''
	'''
	role	= models.ForeignKey(Role, verbose_name=u'Роль')
	jobtit	= models.CharField(max_length=32, verbose_name=u'Должность')

	class   Meta:
		ordering                = ('role', )
		verbose_name            = u'Подписант'
		verbose_name_plural     = u'Подписанты'

	def	__unicode__(self):
		return '%s %s (%s, %s)' % (self.first_name, self.last_name, self.jobtit, self.role.name)

class	File(models.Model):
	'''
	TODO:
	* cache
	* delete
	'''
	filename	= models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Filename')
	mimetype	= models.CharField(max_length=64, verbose_name=u'MIME')
	#size

	def     __unicode__(self):
		return self.filename

	def	get_path(self):
		return os.path.join(settings.BILLS_ROOT, '%08d' % self.pk)

class	Bill(File):
	'''
	Fields:
	?desc:txt
	?ctime:datetime - время создания
	?etime:datetime - время окончания

	??Поставщик
	??Номер счета
	??Дата счета
	??Сумма счета
	TODO:
	* route = ManyToMany(User)
	* history = ManyToMany(User)
	* Object = FK
	* Depart = FK
	#created	= models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')	# editable-False
	#updated	= models.DateTimeField(auto_now=True, verbose_name=u'Изменен')		# editable-False
	TODO: get_route_ok(user):
	* user not in route
	* route ends w/ accounter
	* route len > 0
	'''
	project		= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Объект')
	depart		= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Направление')
	supplier	= models.CharField(max_length=64, verbose_name=u'Поставщик')
	assign		= models.ForeignKey(Approver, related_name='assigned', verbose_name=u'Исполнитель')
	approve		= models.ForeignKey(Approver, related_name='inbox',    verbose_name=u'Согласующий')
	isalive		= models.BooleanField(verbose_name=u'Живой')
	isgood		= models.BooleanField(verbose_name=u'Хороший')
	#route		= SortedManyToManyField(User, null=True, blank=True, through='BillRoute', verbose_name=u'Маршрут', sort_value_field_name='orderno')
	route		= SortedManyToManyField(Approver, null=True, blank=True, related_name='route', verbose_name=u'Маршрут')
	history		= models.ManyToManyField(Approver, null=True, blank=True, related_name='history', through='BillEvent', verbose_name=u'История')

	def     __unicode__(self):
		return self.filename

	def	get_state(self):
		return states[(self.isalive, self.isgood)]

	class   Meta:
		#unique_together		= (('scan', 'type', 'name'),)
		#ordering                = ('id',)
		verbose_name            = u'Счет'
		verbose_name_plural     = u'Счета'

class	BillEvent(models.Model):
	bill	= models.ForeignKey(Bill, verbose_name=u'Счет')
	user	= models.ForeignKey(Approver, verbose_name=u'Подписант')
	ctime	= models.DateTimeField(auto_now_add=True, verbose_name=u'ДатаВремя')
	comment	= models.TextField(null=True, blank=True, verbose_name=u'Камменты')

	def	__unicode__(self):
		return '%s: %s' % (self.user, self.comment)

	class   Meta:
		ordering                = ('ctime',)
		verbose_name            = u'Резолюция'
		verbose_name_plural     = u'Резолюции'
