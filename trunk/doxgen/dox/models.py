# -*- coding: utf-8 -*-

# 1. django
from django.db import models
from django.contrib.auth.models import User

# 2. 3rd party
from treebeard.al_tree import AL_Node

# 3. system
import datetime, json

'''
class	UserExt:
	pass
'''

class   Doc(models.Model):
	user		= models.ForeignKey(User, verbose_name=u'Пользователь')
	created		= models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')	# editable-False
	updated		= models.DateTimeField(auto_now=True, verbose_name=u'Изменен')		# editable-False
	type		= models.CharField(max_length=32, verbose_name=u'Тип')
	name		= models.CharField(max_length=32, verbose_name=u'Наименование')
	data		= models.TextField(verbose_name=u'Данные')

	def     __unicode__(self):
		return self.name

	#def save(self):
	#	if not self.id:
	#		self.created = datetime.date.today()
	#	self.updated = datetime.datetime.today()
	#	super(Doc, self).save()

	@models.permalink
	def get_absolute_url(self):
		return ('dox.views.doc_r', [str(self.id)])

	def get_edit_url(self):
		return reverse('dox.views.doc_u', args=[self.pk])

	def get_del_url(self):
		return reverse('dox.views.doc_d', args=[self.pk])

	class   Meta:
		unique_together		= (('user', 'type', 'name'),)
		ordering                = ('type', 'name', )
		verbose_name            = u'Документ'
		verbose_name_plural     = u'Документы'

class   Log(models.Model):
	date		= models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
	method		= models.BooleanField(verbose_name=u'Метод')
	ip		= models.IPAddressField(verbose_name=u'IP')
	path		= models.CharField(max_length=255, verbose_name=u'Куда')
	agent		= models.CharField(null=True, max_length=255, verbose_name=u'Агент')
	data		= models.TextField(verbose_name=u'Данные')

	def	__unicode__(self):
		return self.ip

	class   Meta:
		ordering                = ('date',)
		verbose_name            = u'Лог'
		verbose_name_plural     = u'Логи'

class	SSRF(models.Model):
	'''
	Справочник Субъектов Российской Федерации
	'''
	name		= models.CharField(max_length=64, verbose_name=u'Наименование')

	def     __unicode__(self):
		return self.name

	class   Meta:
		ordering = ('name',)
		verbose_name = u'ССРФ'
		verbose_name_plural = u'ССРФы'

class   Okved(AL_Node):
	id	= models.CharField(max_length=8, primary_key=True, verbose_name=u'Код')
	parent	= models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Группа')
	name	= models.CharField(max_length=400, blank=False, verbose_name=u'Наименование')
	node_order_by	= ['parent', 'id']

	def     __unicode__(self):
		return u'%s: %s' % (self.id, self.name[:100])

	class   Meta:
		ordering = ('id',)
		#ordering = ('parent', 'id',)
		verbose_name = u'ОКВЭД'
		verbose_name_plural = u'ОКВЭДы'
