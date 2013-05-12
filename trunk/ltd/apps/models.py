# -*- coding: utf-8 -*-
'''
'''

from django.db import models
from django.contrib.auth.models import User
#from settings import LOGIN_REDIRECT_URL

doxcache = {}

class	ODFType(models.Model):
    '''
    Тип ODF
    '''
    id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'ID')
    ext		= models.CharField(max_length=5, null=False, blank=False, verbose_name=u'Расширение')
    mime	= models.CharField(max_length=64, null=False, blank=False, verbose_name=u'MIME')
    icon	= models.CharField(max_length=11, null=False, blank=False, verbose_name=u'Пиктограмма')
    name	= models.CharField(max_length=16, null=False, blank=False, verbose_name=u'Наименование')

    def     __unicode__(self):
                return self.name

    class   Meta:
        verbose_name            = u'Тип шаблона'
        verbose_name_plural     = u'Типы шаблонов'

class	ODFExport(models.Model):
    '''
    Тип экспортов ODF
    '''
    odftype	= models.ForeignKey(ODFType, null=False, blank=False, verbose_name=u'Тип ODF')
    key		= models.CharField(max_length=8, null=False, blank=False, verbose_name=u'Ключ')
    ext		= models.CharField(max_length=4, null=False, blank=False, verbose_name=u'Расширение')
    mime	= models.CharField(max_length=64, null=False, blank=False, verbose_name=u'MIME')
    name	= models.CharField(max_length=32, null=False, blank=False, verbose_name=u'Наименование')

    def     __unicode__(self):
                return u'%s [.%s]' % (self.name, self.ext)

    class   Meta:
        verbose_name            = u'Тип экспорта шаблона'
        verbose_name_plural     = u'Типы экспорта шаблонов'

class	DocType(models.Model):
    '''
    Тип документа
    '''
    id		= models.IntegerField(primary_key=True, verbose_name=u'ID')
    odftype	= models.ForeignKey(ODFType, null=False, blank=False, verbose_name=u'Тип ODF')
    name	= models.CharField(max_length=64, verbose_name=u'Наименование')
    desc	= models.CharField(max_length=255, verbose_name=u'Полностью')

    def     __unicode__(self):
                return self.name

    @models.permalink
    def	get_absolute_url(self):
        return ('apps.views.doc_index', [str(self.id)])

    class   Meta:
#		app_label		= 'doxgen'
        verbose_name            = u'Шаблон'
        verbose_name_plural     = u'Шаблоны'

class	DocEntity(models.Model):
    '''
    Документ
    '''
    type	= models.ForeignKey(DocType, null=False, blank=False, verbose_name=u'Тип документа')
    name	= models.CharField(max_length=32, null=False, blank=False, verbose_name=u'Наименование')
    data	= models.TextField(null=False, blank=False, verbose_name=u'Данные')

    def     __unicode__(self):
        return self.type.name + ": " + self.name

    @models.permalink
    def	get_absolute_url(self):
        return ('apps.views.doc_detail', [str(self.id)])

    def	get_edit_url(self):
        return reverse('apps.views.doc_edit', args=[self.pk])

    def	get_del_url(self):
        return reverse('apps.views.doc_del', args=[self.pk])

    class   Meta:
        ordering                = ('type', 'name', )
        verbose_name            = u'Документ'
        verbose_name_plural     = u'Документы'
