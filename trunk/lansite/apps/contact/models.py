# -*- coding: utf-8 -*-

'''
lansite.apps.contact.models

TODO: Contact - empty + ContactCommon (abstract)
'''

from django.db import models
from django.contrib.auth.models import User
from apps.core.models import *
from apps.ref.models import *
from settings import LOGIN_REDIRECT_URL

class   Contact(Object):
	user	= models.ForeignKey(User, null=True, blank=True, db_index=True, verbose_name=u'Пользователь')
        addr	= models.ManyToManyField(Address,       through='ContactAddr', verbose_name=u'Адреса')
        phone	= models.ManyToManyField(Phone,         through='ContactPhone', verbose_name=u'Телефоны')
        www	= models.ManyToManyField(WWW,           through='ContactWWW', verbose_name=u'WWW')
        email	= models.ManyToManyField(Email,         through='ContactEmail', verbose_name=u'Email')
        im	= models.ManyToManyField(IM,            through='ContactIM', verbose_name=u'IM')

        def     __unicode__(self):
                return u'Contact...'

        def     gettype(self):
                return u'Contact'
            
        def     getaddress(self, type):            
            try:
                contactaddrtype = ContactAddrType.objects.get(name=type)
                address_id = Contact2AddrType.objects.filter(type=contactaddrtype,caddr__in=ContactAddr.objects.filter(contact__id=self.id)).values_list('caddr__addr__id')[0][0]
                address = Address.objects.get(pk=address_id)
            except:
                address = ''   
            return address
        
	@models.permalink
	def	get_absolute_url(self):
		return ('apps.contact.views.contact_detail', [self.pk])

	def	get_edit_url(self):
		return reverse('apps.contact.views.contact_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.contact.views.contact_del', args=[self.pk])

        class   Meta:
                app_label		= 'gw'
                verbose_name            = u'Контакт'
                verbose_name_plural     = u'Контакты'

class   ContactAddrType(models.Model):
        '''
        Тип адреса: Юридический, Фактический
        '''
        id              = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
        name            = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

        def     __unicode__(self):
                return self.name

        class   Meta:
                app_label		= 'gw'
                ordering                = ('name', )
                verbose_name            = u'Тип адреса контакта'
                verbose_name_plural     = u'Типы адресов контактов'

class   ContactAddr(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        addr            = models.ForeignKey(Address, null=False, blank=False, verbose_name=u'Адрес')
        types           = models.ManyToManyField(ContactAddrType, through='Contact2AddrType', verbose_name=u'Типы')

        def     __unicode__(self):
                return u'%s: %s (%s)' % (self.contact, self.addr, self.type)

        class   Meta:
                app_label		= 'gw'
                verbose_name            = u'Контакт.Адрес'
                ordering                = ('contact', 'addr',)
                unique_together         = (('contact', 'addr',),)
                verbose_name_plural     = u'Контакты.Адреса'

class   Contact2AddrType(models.Model):
        type            = models.ForeignKey(ContactAddrType, null=False, blank=False, verbose_name=u'Тип')
        caddr           = models.ForeignKey(ContactAddr, null=False, blank=False, verbose_name=u'Контакт.Адрес')

        def     __unicode__(self):
                return u'%s: %s' % (self.phone, self.type)

        class   Meta:
                app_label		= 'gw'
                verbose_name            = u'Тип адреса контакта'
                verbose_name_plural     = u'Типы адресов контактов'
                ordering                = ('caddr', 'type',)
                unique_together         = (('type', 'caddr',),)

class   ContactPhone(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        phone           = models.ForeignKey(Phone, null=False, blank=False, verbose_name=u'Телефон')
        ext             = models.CharField(max_length=4, null=True, blank=True, verbose_name=u'DTMF')

        def     __unicode__(self):
                return u'%s: %s (%s)' % (self.contact, self.phone, self.ext)

        class   Meta:
                app_label		= 'gw'
                ordering                = ('contact', 'phone',)
                unique_together         = (('contact', 'phone',),)
                verbose_name            = u'Контакт.Телефон'
                verbose_name_plural     = u'Контакты.Телефоны'

class   ContactWWW(models.Model):
        '''
        TODO: URL => www
        '''
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        www             = models.ForeignKey(WWW, null=False, blank=False, verbose_name=u'WWW')

        def     __unicode__(self):
                return u'%s: %s' % (self.contact, self.www)

        class   Meta:
                app_label		= 'gw'
                ordering                = ('contact', 'www',)
                unique_together         = (('contact', 'www',),)
                verbose_name            = u'Контакт.WWW'
                verbose_name_plural     = u'Контакты.WWW'

class   ContactEmail(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        email           = models.ForeignKey(Email, null=False, blank=False, verbose_name=u'Email')

        def     __unicode__(self):
                return u'%s: %s' % (self.contact, self.email)

        class   Meta:
                app_label		= 'gw'
                ordering                = ('contact', 'email',)
                unique_together         = (('contact', 'email',),)
                verbose_name            = u'Контакт.Email'
                verbose_name_plural     = u'Контакты.Email'

class   ContactIM(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        im              = models.ForeignKey(IM, null=False, blank=False, verbose_name=u'IM')

        def     __unicode__(self):
                return u'%s: %s: %s' % (self.contact, self.im.account, self.im.type)

        class   Meta:
                app_label		= 'gw'
                ordering                = ('contact', 'im',)
                unique_together         = (('contact', 'im',),)
                verbose_name            = u'Контакт.IM'
                verbose_name_plural     = u'Контакты.IM'

class    Person(Contact):
	firstname   = models.CharField(max_length=16, blank=False, db_index=True, verbose_name=u'Имя')
	midname     = models.CharField(max_length=24, blank=True, db_index=True, verbose_name=u'Отчество')
	lastname    = models.CharField(max_length=24, blank=True, db_index=True, verbose_name=u'Фамилия')
	birthdate   = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'День рождения')
	sex         = models.BooleanField(null=False, blank=False, default=True, db_index=True, verbose_name=u'Пол')

	def    getfio(self):
		return u'%s %s. %s.' % (self.lastname, self.firstname[:1], self.midname[:1])

	def    __unicode__(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

	def     gettype(self):
		return u'Person'

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.contact.views.person_detail', [self.pk])

	def	get_edit_url(self):
		return reverse('apps.contact.views.person_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.contact.views.person_del', args=[self.pk])

	class    Meta:
		app_label		= 'gw'
		ordering		= ('lastname', 'firstname', 'midname')
		verbose_name		= u'Человек'
		verbose_name_plural	= u'Люди'

class    Org(Contact):
	name       = models.CharField(null=False, blank=False, max_length=40, db_index=True, verbose_name=u'Наименование')
	shortname  = models.CharField(null=True, blank=True, max_length=100, db_index=True, verbose_name=u'Краткое Наименование')
	fullname   = models.CharField(null=True, blank=True, max_length=150, db_index=True, verbose_name=u'Полное наименование')
	brandname  = models.CharField(max_length=128, null=True, blank=True, db_index=True, verbose_name=u'Фирменное наименование')
	egruldate  = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Дата регистрации в ЕГРЮЛ')
	inn        = models.CharField(null=True, blank=True, max_length=12, verbose_name=u'ИНН')
	kpp        = models.CharField(null=True, blank=True, max_length=9, db_index=True, verbose_name=u'КПП')
	ogrn       = models.CharField(null=True, blank=True, max_length=15, db_index=True, verbose_name=u'ОГРН/СГРП')
	okato      = models.ForeignKey(Okato, null=True, blank=True, db_index=True, verbose_name=u'ОКАТО')
	okopf      = models.ForeignKey(Okopf, null=True, blank=True, db_index=True, verbose_name=u'ОКОПФ')
	comments   = models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
	okveds     = models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
	stuffs     = models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')

	def    __unicode__(self):
		return self.name

	def gettype(self):
		return u'Org'

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.contact.views.org_detail', [self.pk])

	def	get_edit_url(self):
		return reverse('apps.contact.views.org_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.contact.views.org_del', args=[self.pk])

	class    Meta:
		app_label = 'gw'
		ordering = ('name',)
		verbose_name        = u'Организация'
		verbose_name_plural    = u'Организации'

class    OrgOkved(models.Model):
    org        = models.ForeignKey(Org, verbose_name=u'Организация')
    okved        = models.ForeignKey(Okved, verbose_name=u'ОКВЭД')

    def    asstr(self):
        return self.okved.asstr()

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        verbose_name        = u'Организация.ОКВЭД'
        verbose_name_plural    = u'Организация.Коды ОКВЭД'
        unique_together        = [('org', 'okved')]

class   JobRole(models.Model):
        name            = models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Наименование')
        comments        = models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

        def     __unicode__(self):
                return self.name

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.contact.views.jobrole_detail', [self.pk])

	def	get_edit_url(self):
		return reverse('apps.contact.views.jobrole_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.contact.views.jobrole_del', args=[self.pk])

        class   Meta:
                app_label = 'gw'
                ordering = ('name',)
                verbose_name = u'Должность'
                verbose_name_plural = u'Должности'

class   OrgStuff(models.Model):
        '''
        TODO: rename to Stuff
        '''
        org             = models.ForeignKey(Org, verbose_name=u'Организация')
        role            = models.ForeignKey(JobRole, verbose_name=u'Должность')
        person          = models.ForeignKey(Person, verbose_name=u'Человек')

        def     __unicode__(self):
                return u'%s, %s: %s' % (self.org, self.role, self.person)

        class   Meta:
                app_label = 'gw'
                verbose_name            = u'Организация.Должностное лицо'
                verbose_name_plural     = u'Организация.Должностные лица'
                unique_together         = [('org', 'role', 'person')]
