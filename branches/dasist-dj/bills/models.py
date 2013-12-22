# -*- coding: utf-8 -*-

# 1. django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# 2. 3rd parties
from sortedm2m.fields import SortedManyToManyField

# 3. system
import os, datetime

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
	'''
	project	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Объект')
	depart	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Направление')
	assign	= models.ForeignKey(User, related_name='assigned', verbose_name=u'Исполнитель')
	approve	= models.ForeignKey(User, related_name='inbox',    verbose_name=u'Согласующий')
	isalive	= models.BooleanField(verbose_name=u'Живой')
	isgood	= models.BooleanField(verbose_name=u'Хороший')
	#route	= SortedManyToManyField(User, null=True, blank=True, through='BillRoute', verbose_name=u'Маршрут', sort_value_field_name='orderno')
	route	= SortedManyToManyField(User, null=True, blank=True, verbose_name=u'Маршрут')

	def     __unicode__(self):
		return self.filename

	class   Meta:
		#unique_together		= (('scan', 'type', 'name'),)
		#ordering                = ('id',)
		verbose_name            = u'Счет'
		verbose_name_plural     = u'Счета'
'''
class	BillRoute(models.Model):
	bill	= models.ForeignKey(Bill, verbose_name=u'Счет')
	user	= models.ForeignKey(User, verbose_name=u'Пользователь')
	orderno	= models.PositiveSmallIntegerField(verbose_name=u'#')
	ctime	= models.DateTimeField(null=True, blank=True, verbose_name=u'ДатаВремя')
	comment	= models.TextField(null=True, blank=True, verbose_name=u'Камменты')

	def	__unicode__(self):
		return self.user

	class   Meta:
		ordering                = ('orderno',)
		verbose_name            = u'ТочкаМаршрута'
		verbose_name_plural     = u'ТочкиМаршрута'
'''
class	Role(models.Model):
	'''
	Predefined role model
	Try: m2m user (via Approver)
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

class	Approver(models.Model):
	'''
	User as Roler
	Try: inherit User
	'''
	user	= models.OneToOneField(User, primary_key=True, verbose_name=u'Юзверь')
	role	= models.ForeignKey(Role, verbose_name=u'Роль')

	class   Meta:
		unique_together		= (('user', 'role',),)
		ordering                = ('user', )
		verbose_name            = u'РольПользователя'
		verbose_name_plural     = u'РолиПользователей'

	def	__unicode__(self):
		return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.role.name)

