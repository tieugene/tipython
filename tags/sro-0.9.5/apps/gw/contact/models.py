# -*- coding: utf-8 -*-

'''
lansite.gw.task.models.py

Multitask: subtasks w/o subj, desk, etc - just assignee, state
'''

from django.db import models
from django.contrib.auth.models import User
from apps.gw.bits.models import *
from settings import LOGIN_REDIRECT_URL



class   Contact(Object):
        addr            = models.ManyToManyField(Address,       through='ContactAddr', verbose_name=u'Адреса')
        phone           = models.ManyToManyField(Phone,         through='ContactPhone', verbose_name=u'Телефоны')
        www             = models.ManyToManyField(WWW,           through='ContactWWW', verbose_name=u'WWW')
        email           = models.ManyToManyField(Email,         through='ContactEmail', verbose_name=u'Email')
        im              = models.ManyToManyField(IM,            through='ContactIM', verbose_name=u'IM')

#       def     __unicode__(self):
#               return self.name
        def get_absolute_url(self):
            return LOGIN_REDIRECT_URL+"gw/contact/%i/" % self.id

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
        
        class   Meta:
                app_label = 'gw'
                verbose_name            = u'Контакт'
                verbose_name_plural     = u'Контакты'

class   ContactAddrType(models.Model):
        '''
        Тип адреса: Юридический, Фактический
        '''
        id              = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
        name            = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

        def     asstr(self):
                return self.name

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                ordering                = ('name', )
                verbose_name            = u'Тип адреса контакта'
                verbose_name_plural     = u'Типы адресов контактов'

class   ContactAddr(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        addr            = models.ForeignKey(Address, null=False, blank=False, verbose_name=u'Адрес')
        types           = models.ManyToManyField(ContactAddrType, through='Contact2AddrType', verbose_name=u'Типы')

        def     asstr(self):
                return u'%s: %s (%s)' % (self.contact, self.addr, self.type)

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                verbose_name            = u'Контакт.Адрес'
                ordering                = ('contact', 'addr',)
                unique_together         = (('contact', 'addr',),)
                verbose_name_plural     = u'Контакты.Адреса'

class   Contact2AddrType(models.Model):
        type            = models.ForeignKey(ContactAddrType, null=False, blank=False, verbose_name=u'Тип')
        caddr           = models.ForeignKey(ContactAddr, null=False, blank=False, verbose_name=u'Контакт.Адрес')

        def     asstr(self):
                return u'%s: %s' % (self.phone, self.type)

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                verbose_name            = u'Тип адреса контакта'
                verbose_name_plural     = u'Типы адресов контактов'
                ordering                = ('caddr', 'type',)
                unique_together         = (('type', 'caddr',),)

class   ContactPhone(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        phone           = models.ForeignKey(Phone, null=False, blank=False, verbose_name=u'Телефон')
        ext             = models.CharField(max_length=4, null=True, blank=True, verbose_name=u'DTMF')

        def     asstr(self):
                return u'%s' % (self.phone)

        def     __unicode__(self):
                return u'%s: %s (%s)' % (self.contact, self.phone, self.ext)

        class   Meta:
                app_label = 'gw'
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

        def     asstr(self):
                return u'%s' % (self.www)

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                ordering                = ('contact', 'www',)
                unique_together         = (('contact', 'www',),)
                verbose_name            = u'Контакт.WWW'
                verbose_name_plural     = u'Контакты.WWW'

class   ContactEmail(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        email           = models.ForeignKey(Email, null=False, blank=False, verbose_name=u'Email')

        def     asstr(self):
                return u'%s' % (self.email)

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                ordering                = ('contact', 'email',)
                unique_together         = (('contact', 'email',),)
                verbose_name            = u'Контакт.Email'
                verbose_name_plural     = u'Контакты.Email'

class   ContactIM(models.Model):
        contact         = models.ForeignKey(Contact, null=False, blank=False, verbose_name=u'Контакт')
        im              = models.ForeignKey(IM, null=False, blank=False, verbose_name=u'IM')

        def     asstr(self):
                return u'%s: %s: %s' % (self.contact, self.im.account, self.im.type)

        def     __unicode__(self):
                return self.asstr()

        class   Meta:
                app_label = 'gw'
                ordering                = ('contact', 'im',)
                unique_together         = (('contact', 'im',),)
                verbose_name            = u'Контакт.IM'
                verbose_name_plural     = u'Контакты.IM'

class    Okato(models.Model):
    #
    #id - by OKATO
    #

    id        = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=100, blank=False, unique=False, verbose_name=u'Наименование')

    def    asstr(self):
        return u'%d: %s' % (self.id, self.name)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        ordering = ('id',)
        verbose_name = u'ОКАТО'
        verbose_name_plural = u'ОКАТО'

class    Okopf(AL_Node):
    #
    #id - by OKOPF, short int
    #
    id        = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
    shortname    = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Краткое наименование')
    namedp        = models.CharField(max_length=100, blank=True, unique=False, verbose_name=u'Наименование (д.п.)')
    disabled    = models.BooleanField(blank=False, verbose_name=u'Не выбирать')
    parent        = models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Предок')
    node_order_by    = ['id']

    def    asstr(self):
        if (self.shortname):
            return "%s: %s" % (self.shortname, self.name)
        else:
            return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        ordering = ('id',)
        verbose_name = u'ОКОПФ'
        verbose_name_plural = u'ОКОПФ'

class    Okved(AL_Node):
    #
    #id - by OKVED, str
    #
    id        = models.CharField(max_length=6, primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=400, blank=False, unique=False, verbose_name=u'Наименование')
    parent        = models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Предок')
    node_order_by    = ['id']

    def    fmtid(self):
        l = len(self.id)
        if (l < 3):
            return id
        elif (l > 4):
            return u'%s.%s.%s' % (self.id[:2], self.id[2:4], self.id[4:])
        else:
            return u'%s.%s' % (self.id[:2], self.id[2:])

    def    asstr(self):
        return u'%s %s' % (self.fmtid(), self.name[:100])

    def    asshortstr(self):
        if (len(self.name) > 50):
            s = self.name[:50] + "<br/>" + self.name[50:]
        else:
            s = self.name
        return u'%s - %s' % (self.fmtid(), s)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        ordering = ('id',)
        verbose_name = u'ОКВЭД'
        verbose_name_plural = u'ОКВЭД'

class    Speciality(ExtraObject,models.Model):
    name        = models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()


    def get_absolute_url(self):
        return ''
    
    class    Meta:
        app_label = 'gw'
        ordering    = ('name',)
        verbose_name    = u'Специальность'
        verbose_name_plural = u'Специальности'


class    Skill(ExtraObject,models.Model):
    name        = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
    high        = models.BooleanField(blank=False, null=False, default=False, verbose_name=u'Высшее')

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()


    def get_absolute_url(self):
        return ''        

    class    Meta:
        app_label = 'gw'
        ordering = ('name',)
        verbose_name = u'Квалификация'
        verbose_name_plural = u'Квалификации'


class    Role(ExtraObject,models.Model):
    name        = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
    comments    = models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

    def    asstr(self):
        retvalue = self.name
        if self.comments:
            retvalue += u' (%s)' % self.comments
        return retvalue

    def    __unicode__(self):
        return self.asstr()

    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"admin/gw/role/%i/" % self.id

    class    Meta:
        app_label = 'gw'
        ordering = ('name',)
        verbose_name = u'Должность'
        verbose_name_plural = u'Должности'

class    Person(ExtraObject,Contact):
    firstname   = models.CharField(max_length=16, blank=False, db_index=True, verbose_name=u'Имя')
    midname     = models.CharField(max_length=24, blank=True, db_index=True, verbose_name=u'Отчество')
    lastname    = models.CharField(max_length=24, blank=False, db_index=True, verbose_name=u'Фамилия')
    skills      = models.ManyToManyField(Skill, through='PersonSkill', verbose_name=u'Квалификации')
    user       = models.ForeignKey(User, null=True, blank=True, db_index=True, verbose_name=u'Пользователь1')
    birthdate   = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'День рождения')
    sex         = models.BooleanField(null=False, blank=False, default=True, db_index=True, verbose_name=u'Пол')

    def    asstr(self):
        return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

    def    getfio(self):
        return u'%s %s. %s.' % (self.lastname, self.firstname[:1], self.midname[:1])

    def    __unicode__(self):
        return self.asstr()

    def     gettype(self):
        return u'Person'


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+'sro2/person/%i' % self.id    

    class    Meta:
        app_label = 'gw'
        ordering = ('lastname', 'firstname', 'midname')
        verbose_name = u'Сотрудник'
        verbose_name_plural = u'Сотрудники'

class    PersonSkill(ExtraObject,models.Model):
    person        = models.ForeignKey(Person, verbose_name=u'Человек')
    speciality    = models.ForeignKey(Speciality, verbose_name=u'Специальность')
    skill        = models.ForeignKey(Skill, verbose_name=u'Квалификация')
    year        = models.PositiveIntegerField(null=False, blank=False, default=0, verbose_name=u'Год')
    skilldate    = models.DateField(null=True, blank=True, verbose_name=u'Дата окончания')
    school        = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'Учебное заведение')
    seniority    = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Стаж')
    seniodate    = models.DateField(null=True, blank=True, verbose_name=u'Дата актуальности стажа')
    tested        = models.DateField(null=True, blank=True, verbose_name=u'Дата последней аттестации')


    def get_absolute_url(self):
        return self.person.get_absolute_url()

    def    asstr(self):
        return u'%s: %s, %s' % (self.person.asstr(), self.speciality.asstr(), self.skill.asstr())

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        verbose_name = u'Квалификация сотрудника'
        verbose_name_plural = u'Квалификации сотрудника'

class    Course(ExtraObject,models.Model):
    personskill    = models.ForeignKey(PersonSkill, verbose_name=u'Квалификация')
    courseno    = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'СоПК.№')
    coursedate    = models.DateField(null=False, blank=False, verbose_name=u'СоПК.Дата Выдачи')
    coursename    = models.CharField(max_length=150, null=True, blank=True, verbose_name=u'СоПК.Наименование курсов')
    courseschool    = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'СоПК.УЗ')
    def    asstr(self):
        return u'%s №%s от %s (%s)' % (self.coursename,self.courseno,self.coursedate,self.courseschool)

    def __unicode__(self):
        return self.asstr()

    def get_absolute_url(self):
        return self.personskill.person.get_absolute_url()    
    class    Meta:
        app_label = 'gw'
        verbose_name = u'СоПК'


class    Org(ExtraObject,Contact):
    name       = models.CharField(null=False, blank=False, max_length=40, unique=False, db_index=True, verbose_name=u'Отображаемое наименование')
    shortname  = models.CharField(null=False, blank=False, max_length=100, unique=False, db_index=True, verbose_name=u'Краткое Наименование')
    fullname   = models.CharField(null=False, blank=False, max_length=150, unique=False, db_index=True, verbose_name=u'Полное наименование')
    okopf      = models.ForeignKey(Okopf, null=False, blank=False, db_index=True, verbose_name=u'ОКОПФ')
    egruldate  = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Дата регистрации в ЕГРЮЛ')
    inn        = models.CharField(null=False, blank=False, max_length=12, unique=True, verbose_name=u'ИНН')
    kpp        = models.CharField(null=True, blank=True, max_length=9, db_index=True, verbose_name=u'КПП')
    foreign    = models.BooleanField(null=False, blank=False, default=False, db_index=True, verbose_name=u'Иностранная организация') # 0: Russian, 1: foreign
    ogrn       = models.CharField(null=False, blank=False, max_length=15, unique=True, verbose_name=u'ОГРН/СГРП')
    okato      = models.ForeignKey(Okato, null=True, blank=True, db_index=True, verbose_name=u'ОКАТО')
    laddress   = models.CharField(null=False, blank=True, max_length=255, verbose_name=u'Адрес юридический')
    raddress   = models.CharField(null=False, blank=True, max_length=255, verbose_name=u'Адрес почтовый')
    comments   = models.TextField(null=True, blank=True, verbose_name=u'Комментарии')
    user       = models.ForeignKey(User, null=True, blank=True, db_index=True, verbose_name=u'Пользователь')
    okveds     = models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
    stuffs     = models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')
    brandname  = models.CharField(max_length=128, null=True, blank=True, db_index=True, verbose_name=u'Фирменное наименование')


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+'sro2/org/%i' % self.id
    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    def __ogrn_label(self):
        if self.foreign:
            return u'Свидетельство государственной регистрационной палаты №'
        else:
            return u'ОГРН'

    def __ogrn_shortlabel(self):
        if self.foreign:
            return u'СГРП №'
        else:
            return u'ОГРН'

    def gettype(self):
        return u'Org'

    ogrn_label = property(__ogrn_label)
    ogrn_shortlabel = property(__ogrn_shortlabel)

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

class    OrgStuff(ExtraObject,models.Model):
    '''
    FIXME: permanent => Fulltime job
    '''
    org        = models.ForeignKey(Org, verbose_name=u'Организация')
    role        = models.ForeignKey(Role, verbose_name=u'Должность')
    person        = models.ForeignKey(Person, verbose_name=u'Человек')
    leader        = models.BooleanField(default=False, verbose_name=u'Руководитель')
    permanent    = models.BooleanField(default=False, verbose_name=u'Основное')
    startdate    = models.DateField(null=True, blank=True, verbose_name=u'Дата принятия на работу')
    enddate    = models.DateField(null=True, blank=True, verbose_name=u'Дата увольнения')

    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+'sro2/person/%i' % self.person.id
    def    asstr(self):
        return u'%s: %s' % (self.role.asstr(), self.person.asstr())

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        app_label = 'gw'
        verbose_name        = u'Организация.Должностное лицо'
        verbose_name_plural    = u'Организация.Должностные лица'
        unique_together        = [('org', 'role', 'person')]
