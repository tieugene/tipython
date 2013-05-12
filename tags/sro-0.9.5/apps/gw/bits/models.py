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

from apps.sro2.mid import get_request

from django.contrib.contenttypes.models import ContentType

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from settings import LOGIN_REDIRECT_URL



class Change(models.Model):
    journal=models.ForeignKey(LogEntry, verbose_name=u'Запись журнала')
    username=models.CharField(max_length=40, verbose_name=u'ФИО пользователя')
    field=models.CharField(max_length=255, verbose_name=u'Измененное поле')
    previuos=models.CharField(max_length=255, verbose_name=u'Прошлое значение')
    present=models.CharField(max_length=255, verbose_name=u'Настоящее значение')

    def __unicode__(self):
        return '<b>%s</b>:<br> c "<b>%s</b>" на "<b>%s</b>"' % (self.field,self.previuos,self.present)

    class    Meta:
        app_label = 'gw'
        ordering = ('id',)
        verbose_name = u'Изменение данных'

def	log_it(request, object, action='',change_message=''):
    '''
    Log this activity
    '''
    if object.pk is None and not action:
        action=ADDITION
    elif not action:
        action=CHANGE
    LogEntry.objects.log_action(
        user_id		 = request.user.id,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id	   = object.pk,
        object_repr	 = object.asstr(), # Message you want to show in admin action list
        change_message  = u'SRO2.UI: ' + change_message, # I used same
        action_flag	 = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
    )
    if action == CHANGE:
        try:
            pres_object=object.__class__.objects.get(pk=object.pk)
        except:
            action=ADDITION
    if action == CHANGE:
        for prop in object.__dict__.keys():
            try:
                j=LogEntry.objects.latest('action_time')
                n=Change.objects.all().count()+1
                if not prop.startswith('_') and str(object.__dict__[prop])!= str(pres_object.__dict__[prop]):
                    present=str(pres_object.__dict__[prop])
                    new=str(object.__dict__[prop])
                    try:
                        field=object._meta.get_field(prop).verbose_name
                    except:
                        try:
                            field=object._meta.get_field(prop[0:-3]).verbose_name
                            if not getattr(pres_object,prop[0:-3]) is None:
                                present=getattr(pres_object,prop[0:-3]).asstr()
                            if not getattr(object,prop[0:-3]) is None:
                                new=getattr(object,prop[0:-3]).asstr()
                        except:
                            field=prop
                    ch=Change(
                            n,
                            j.id,
                            u'%s %s' % (request.user.first_name,request.user.last_name),
                            field,
                            present,
                            new,
                            )
                    ch.save()
                    n+=1
            except Exception,e:
                raise Exception('[%s] %s -- %s \n%s' % (prop, str(pres_object.__dict__[prop]), str(object.__dict__[prop]),e))
    return action


class ExtraObject(object):
    def save(self, force_insert = False, force_update = False, action='', using=''):
        if not action:
            action=log_it(get_request(), self)
        else:
            log_it(get_request(), self,action)
        if issubclass(self.__class__,PolymorphicModel):
            PolymorphicModel.save(self,force_insert = force_insert, force_update = force_update)
        else:
            models.Model.save(self,force_insert = force_insert, force_update = force_update, using=using)

        if action==ADDITION or action==4:
            log=LogEntry.objects.latest('action_time')
            log.object_id=self.id
            log.save()
        return

    def delete(self):
#        raise Exception('boom')
        log_it(get_request(), self,DELETION)
        models.Model.delete(self)
        return

    def get_journal_url(self):
        ctype=ContentType.objects.get_for_model(self.__class__)
        return LOGIN_REDIRECT_URL+"sro2/journal/%s/%i/" % (ctype.model,self.id)


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
        if (o is None):
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
    General lansite parent.
    '''
    links	= models.ManyToManyField('self', symmetrical=False, through='ObjectLink', verbose_name=u'Объекты')

    def get_absolute_url(self):
        return ''

    class	Meta:
        app_label		= 'gw'
        verbose_name		= u'Объект'
        verbose_name_plural	= u'Объекты'

class	ObjectLink(models.Model):
    '''
    master		= models.ForeignKey(Object, related_name='slave', verbose_name=u'Хозяин')
    slave		= models.OneToOneField(Object, related_name='master', primary_key=True, verbose_name=u'Объект')
    '''
    left		= models.ForeignKey(Object, related_name='rights', verbose_name=u'Слева')
    right		= models.ForeignKey(Object, related_name='lefts', verbose_name=u'Справа')

    class	Meta:
        app_label = 'gw'
        unique_together		= (('left', 'right',),)
        verbose_name		= u'Связь'
        verbose_name_plural	= u'Связи'

"""
class	ObjectSq(Object):
    '''
    Object sequence.
    Methods: push, pop, swap[, insert, delete]
    '''
    '''
    child	= models.ManyToManyField('self', symmetrical=False, through='SubObject', verbose_name=u'Объекты')
    '''

    class	Meta:
        app_label		= 'gw'
        verbose_name		= u'Последовательность объектов'
        verbose_name_plural	= u'Последовательности объектов'
"""
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
    zip		    = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Индекс')
    fullname	= models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Полный адрес')
    can_delete  = models.BooleanField(null=False, blank=False, default=True, verbose_name=u'Можно удалять')
    node_order_by	= ['name']

    def	__unicode__(self):
        return self.name

    def	asfullstr(self):
        retvalue = u''
        for i in self.getparents():
            retvalue = retvalue + i.name + ', '
        return retvalue + self.name

    def	mkfullname(self, country, zip):
        '''
        Build full name recursively
        '''
        list_without_dot = ['Край']

        if self.endpoint:
            tmp = list()
            for i in self.get_ancestors():
                if i.publish:
                    if i.type:
                        if i.type.name in list_without_dot:
                            tmp.append(i.type.name + u' ' + i.name)
                        else:
                            tmp.append(i.type.name + '. ' + i.name)
                    else:
                        if country:
                            tmp.append(i.name)
                        elif not (i.parent is None):
                            tmp.append(i.name)
            if self.publish:
                if self.type:
                    tmp.append(self.type.name + u'. ' + self.name)
                else:
                    tmp.append(self.name)
            fullname = ', '.join(tmp)
        else:
            fullname = self.name
        if zip and self.zip:
            fullname = str(self.zip) + ', ' + fullname
        self.fullname = fullname
        return self.fullname

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

class	Phone(ExtraObject,Object):
    '''
    Телефонный номер.
    '''
    no		= models.CharField(max_length=15, null=False, blank=False, unique=True, verbose_name=u'Номер')
    types		= models.ManyToManyField(PhoneType, through='Phone2Type', verbose_name=u'Типы')

    def	asstr(self):
        return self.no

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

class	WWW(ExtraObject,Object):
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

class	Email(ExtraObject,Object):
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
