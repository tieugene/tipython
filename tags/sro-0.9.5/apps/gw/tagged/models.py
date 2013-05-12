# -*- coding: utf-8 -*-
'''
TODO: all of MIME types: audio, image, text, video
(option: application, example, message, model, multipart
'''

# 1. django
from django.db import models

# 2. system

# 3. 3rd party

# 4. local
from apps.gw.bits.models import *
from django.contrib.contenttypes.models import ContentType
#from apps.gw.tagged.forms import ObjectListForm

class    TaggedObjectType(models.Model):
    '''
    Attributed Object types
    '''
    name        = models.CharField        (null=False, blank=False, max_length=64, unique=True, verbose_name=u'Наименование')
    comments    = models.CharField        (null=True, blank=True, max_length=255, verbose_name=u'Комментарий')

    def    __unicode__(self):
        return self.name

    class    Meta:
        app_label = 'gw'
        verbose_name = u'Тип теганутых объектов'
        verbose_name_plural = u'Типы теганутых объектов'

class    TaggedObjectTagType(models.Model):
    '''
    Attributes definitions for TaggedObjectType
    Type: str, bool, int, float, decimal, date, time, datetime, ... - all of Django's *Field
    FK: ct_id
    '''
    name = models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Название')
    tot        = models.ForeignKey(TaggedObjectType, null=False, blank=False, verbose_name=u'Тип объекта')
    type        = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'Тип тега')
    multiplicity    = models.PositiveSmallIntegerField(null=False, blank=False, default=0, verbose_name=u'Множественность')    # ?|1|+|*
    options        = models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Опции')    # CommaSeparated* ?

    class    Meta:
        app_label = 'gw'
        verbose_name = u'Тип тэга теганутого объекта'
        verbose_name_plural = u'Типы тэгов теганутых объектов'

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

class    TaggedObject(models.Model):
    '''
    Object with user-defined attributes.
    Not inherits Object because need handle already existant Object
    '''
    object        = models.OneToOneField(Object, related_name='master', primary_key=True, verbose_name=u'Объект', null=False, blank=True)
    tot        = models.ForeignKey(TaggedObjectType, null=False, blank=False, verbose_name=u'Тип')
    tags        = models.ManyToManyField(TaggedObjectTagType, through='TaggedObjectTag', verbose_name=u'Атрибуты', null=True, blank=True)

    class    Meta:
        app_label = 'gw'
        verbose_name = u'Теганутый объект'
        verbose_name_plural = u'Теганутые объекты'

    def __unicode__(self):
        return '%s (%s)' % (self.object, self.tot)



class    TaggedObjectTag(Object):
    '''
    Tags of TaggedObject
    '''
    object        = models.ForeignKey(TaggedObject, null=True, blank=True, verbose_name=u'Объект')
    type        = models.ForeignKey(TaggedObjectTagType, null=False, blank=False, verbose_name=u'Тип')
    value        = models.CharField(null=False, blank=True, max_length=255, verbose_name=u'Значение')

    class    Meta:
        app_label = 'gw'
        verbose_name = u'Атрибут теганутого объекта'
        verbose_name_plural = u'Атрибуты теганутых объектов'

    def __unicode__(self):
        return '%s -- %s' %(self.type,self.value)
