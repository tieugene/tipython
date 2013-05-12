# -*- coding: utf-8 -*-

'''
lansite.gw.models.py
'''

#from django.db.models import Q

from bits.models import *
from contact.models import *
#from task.models import *
from file.models import *
from tagged.models import *
from _mysql import result
from django.db.models.fields import PositiveIntegerField, PositiveSmallIntegerField

class    WordCombination(models.Model):
    nominative      = models.CharField(max_length=255, null=False, blank=False,  verbose_name=u'Именительный падеж', unique=True)
    genetive        = models.CharField(max_length=255, null=False, blank=True,   verbose_name=u'Родительный падеж')
    dative          = models.CharField(max_length=255, null=False, blank=True,   verbose_name=u'Дательный падеж')
    accusative      = models.CharField(max_length=255, null=False, blank=True,   verbose_name=u'Винительный падеж')
    instrumental    = models.CharField(max_length=255, null=False, blank=True,   verbose_name=u'Творительный падеж')
    prepositional   = models.CharField(max_length=255, null=False, blank=True,   verbose_name=u'Предложный падеж')


    def    asstr(self):
        return u'%s' % (self.nominative)

    def    __unicode__(self):
        return self.asstr()

    def __repr__(self):
        return self.asstr()

    def get_case(self):
        result = {}
        if self.nominative:
            result[u'И'] = self.nominative
        if self.genetive:
            result[u'Р'] = self.genetive.lower()
        else:
            result[u'Р'] = self.nominative.lower()
        if self.dative:
            result[u'Д'] = self.dative.lower()
        else:
            result[u'Д'] = self.nominative.lower()
        if self.accusative:
            result[u'В'] = self.accusative.lower()
        else:
            result[u'В'] = self.nominative.lower()
        if self.instrumental:
            result[u'Т'] = self.instrumental.lower()
        else:
            result[u'Т'] = self.nominative.lower()
        if self.prepositional:
            result[u'П'] = self.prepositional.lower()
        else:
            result[u'П'] = self.nominative.lower()
        return result

    def get_shortcase(self):
        try:
            result = {}
            if self.nominative:
                data = self.nominative.split(' ')
                result[u'И'] = '%s %s.%s.' % (data[0], data[1][0], data[2][0])
            if self.genetive:
                result[u'Р'] = self.genetive
            else:
                result[u'Р'] = self.nominative.lower()
            if self.dative:
                result[u'Д'] = self.dative
            else:
                result[u'Д'] = self.nominative.lower()
            if self.accusative:
                result[u'В'] = self.accusative
            else:
                result[u'В'] = self.nominative.lower()
            if self.instrumental:
                result[u'Т'] = self.instrumental
            else:
                result[u'Т'] = self.nominative.lower()
            if self.prepositional:
                result[u'П'] = self.prepositional
            else:
                result[u'П'] = self.nominative.lower()
        except:
            result = self.get_case()
        return result

    class    Meta:
        ordering = ('nominative',)
        verbose_name = u'Словосочетание'
        verbose_name_plural = u'Словосочетания'

class    Permissions(models.Model):
    model = models.ForeignKey(ContentType, null=False, blank=False, verbose_name=u'Моель')
    object      = PositiveIntegerField(null=False, blank=True, default=0, verbose_name=u'Объект')
    subject     = PositiveIntegerField(null=False, blank=False, verbose_name=u'Группа/Пользователь')
    is_user     = models.BooleanField(blank=False, verbose_name=u'Это пользователь')
    perm        = PositiveSmallIntegerField(null=False, blank=False, default=0, verbose_name=u'Права')
    forbid      = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Это запрещающее правило')

    def    asstr(self):
        return u'%s.%s' % (self.model, self.object)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        ordering = ('model','object')
        verbose_name = u'Право'
        verbose_name_plural = u'Права'
        unique_together = [('model', 'object', 'subject')]
