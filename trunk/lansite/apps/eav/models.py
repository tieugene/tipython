# -*- coding: utf-8 -*-
'''
TODO: rename to EAV (Entity-attribute-value) => tune gw_extras, file
'''

# 1. django
from django.db import models

# 2. system

# 3. 3rd party

# 4. local
from apps.core.models import *
from django.contrib.contenttypes.models import ContentType
#from apps.tagged.forms import ObjectListForm

class    TaggedObjectType(models.Model):
	'''
	Attributed Object types - user defined
	FIXME: rename to EAV_EntityType
	'''
	name        = models.CharField        (null=False, blank=False, max_length=64, unique=True, verbose_name=u'Наименование')
	comments    = models.CharField        (null=True, blank=True, max_length=255, verbose_name=u'Комментарий')

	def    __unicode__(self):
		return self.name

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.eav.views.entitytype_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.eav.views.entitytype_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.eav.views.entitytype_del', [str(self.pk)])

	class    Meta:
		app_label = 'gw'
		verbose_name = u'EAV тип Entity'
		verbose_name_plural = u'EAV типы Entity'

class    TaggedObjectTagType(models.Model):
	'''
	Attributes definitions for TaggedObjectType
	Type: str, bool, int, float, decimal, date, time, datetime, ... - all of Django's *Field
	FK: ct_id
	FIXME: rename to EAV_Attribute
	'''
	name		= models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Название')
	tot		= models.ForeignKey(TaggedObjectType, null=False, blank=False, verbose_name=u'Тип объекта')
	type		= models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'Тип тега')
	multiplicity	= models.PositiveSmallIntegerField(null=False, blank=False, default=0, verbose_name=u'Множественность')    # ?|1|+|*
	options		= models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Опции')    # CommaSeparated* ?

	def mult_mark(self):
		marks=['?','1','+','*']
		return marks[self.multiplicity]

	def type_name(self):
		names=[u'Строка',u'Триггер',u'Число',u'Дата',u'Объект']
		name=names[self.type]
		if self.type==4:
		    try:
			name+=' %s' % ContentType.objects.get(id=self.options).name
		    except:
			name='error object id'
		return name

	def type_class(self):
		classes=[u'str',u'bool',u'int',u'date',u'object',u'']
		return classes[self.type]

	def __unicode__(self):
		return '%s (%s) [%s]' % (self.name, self.type_name(),self.mult_mark())

	def get_control(self):
		if self.type_class()=='bool':
		    intype='checkbox'

		else:
		    intype='text'
		options=''
		return '<input type="%s" id="%s" class="%s" %s>'  % (intype,self.id,self.type_class(),options)

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.eav.views.attribute_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.eav.views.attribute_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.eav.views.attribute_del', [str(self.pk)])

	class    Meta:
		app_label = 'gw'
		verbose_name = u'EAV Атрибут'
		verbose_name_plural = u'EAV Атрибуты'

class    TaggedObject(models.Model):
	'''
	Object with user-defined attributes.
	Not inherits Object because need handle already existant Object
	FIXME: rename to EAV_Entity
	'''
	object	= models.OneToOneField(Object, related_name='master', primary_key=True, verbose_name=u'Объект', null=False, blank=True)
	tot		= models.ForeignKey(TaggedObjectType, null=False, blank=False, verbose_name=u'Тип')
	tags	= models.ManyToManyField(TaggedObjectTagType, through='TaggedObjectTag', verbose_name=u'Атрибуты', null=True, blank=True)

	def __unicode__(self):
		return '%s (%s)' % (self.object, self.tot)

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.eav.views.entity_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.eav.views.entity_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.eav.views.entity_del', [str(self.pk)])

	class    Meta:
		app_label = 'gw'
		verbose_name = u'EAV Entity'
		verbose_name_plural = u'EAV Entities'

class    TaggedObjectTag(Object):
	'''
	Tags of TaggedObject
	FIXME: rename to EAV_Value
	'''
	object	= models.ForeignKey(TaggedObject, null=True, blank=True, verbose_name=u'Объект')
	type	= models.ForeignKey(TaggedObjectTagType, null=False, blank=False, verbose_name=u'Тип')
	value	= models.CharField(null=False, blank=True, max_length=255, verbose_name=u'Значение')

	def __unicode__(self):
		return '%s -- %s' %(self.type,self.value)

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.eav.views.value_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.eav.views.value_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.eav.views.value_del', [str(self.pk)])

	class    Meta:
		app_label = 'gw'
		verbose_name = u'EAV Value'
		verbose_name_plural = u'EAV Values'
