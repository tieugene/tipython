# -*- coding: utf-8 -*-
'''
SRO2
'''

import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict
from polymorphic import PolymorphicModel, PolymorphicManager
from treebeard.al_tree import AL_Node
from mid import get_request
###(1
from gw.models import *
###1)
#import pprint
from apps.gw.models import WordCombination
from apps.gw.contact.models import Org
#from apps.sro2.shared import log_it
from django.contrib.contenttypes.models import ContentType

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

def    strdatedot(date):
    if date:
        date = str(date).split('-')
        date ='%s.%s.%s' % (date[2], date[1], date[0])
    return date

def    checkuser(item, user):
    '''
    Check wether user can change this object.
    Can: if user in center branch or in same branch as item.user
    '''
    return (((user.branchuser is not None) and user.branchuser.branch.center) or ((item.user is not None) and item.user.branchuser and user.branchuser and (item.user.branchuser.branch == user.branchuser.branch)))




def    checkuser_speccase(user):
    '''
    Check is user consists in group "SpecialCase"
    '''
    speccase = False

    for group in user.groups.all():
        if (str(group) == 'SpecialCase'):
            speccase = True
            break
    return ((user.is_superuser) or speccase)


class    Branch(models.Model):
    id        = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Наименование')
    center        = models.BooleanField(blank=False, default=False, verbose_name=u'Центральный')

    def get_absolute_url(self):
        return ''

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('name',)
        verbose_name = u'Филиал'
        verbose_name_plural = u'Филиалы'


class    BranchUser(models.Model):
    branch        = models.ForeignKey(Branch, null=False, blank=False, verbose_name=u'Филиал')
    user        = models.OneToOneField(User, null=False, blank=False, verbose_name=u'Пользователь')

    def    asstr(self):
        return u'%s.%s' % (self.branch, self.user)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('branch', 'user',)
        verbose_name = u'Пользователь в филиале'
        verbose_name_plural = u'Пользователи в филиалах'
        unique_together        = (('branch', 'user'),)


class    Insurer(models.Model):
    name        = models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
    fullname    = models.CharField(max_length=100, blank=True, unique=False, verbose_name=u'Полное наименование')

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('name',)
        verbose_name = u'Страховщик'
        verbose_name_plural = u'Страховщики'

class    SroType(models.Model):
    id        = models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')

    def get_absolute_url(self):
        return ''

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('id',)
        verbose_name = u'Тип СРО'
        verbose_name_plural = u'Типы СРО'

class    Sro(ExtraObject,models.Model):
    #name          = models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Краткое наименование')
    #fullname      = models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Полное наименование')
    name          = models.ForeignKey(WordCombination, related_name='sro_name_set', verbose_name=u'Краткое наименование')
    fullname      = models.ForeignKey(WordCombination, related_name='sro_fullname_set', verbose_name=u'Полное наименование')
    displayname   = models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Отображаемое наименование')
    regno         = models.CharField(max_length=20, blank=False, unique=True, verbose_name=u'Рег. №')
    type          = models.ForeignKey(SroType, blank=False, verbose_name=u'Тип')
    own           = models.BooleanField(blank=False, default=False, verbose_name=u'Своё')
    address       = models.CharField(null=False, blank=False, max_length=255, verbose_name=u'Юридический адрес')


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/sro/view/%i/" % self.id        
    def    asstr(self):
        return self.name.asstr()

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
    #    ordering = ('name',)
        verbose_name = u'СРО'
        verbose_name_plural = u'СРО'

class    SroOwn(ExtraObject,models.Model):
    sro              = models.OneToOneField(Sro, verbose_name=u'СРО')
    effector         = models.ForeignKey(WordCombination, related_name='sroown_effector_set', verbose_name=u'Наименование исполнительного органа СРО')
    manage           = models.ForeignKey(WordCombination, related_name='sroown_manage_set', verbose_name=u'Наименование постоянно действующего коллегиального органа управления СРО')
    managechief      = models.ForeignKey(WordCombination, related_name='sroown_managechief_set', verbose_name=u'Наименование руководителя постоянно действующего коллегиального органа управления СРО')
    effectorfull     = models.ForeignKey(WordCombination, related_name='sroown_neffectorfull_set', verbose_name=u'ФИО исполнительного органа СРО (полное)')
    managefull       = models.ForeignKey(WordCombination, related_name='sroown_managefull_set', verbose_name=u'ФИО руководителя постоянно действующего коллегиального органа управления СРО (полное)')
    managedeputyfull = models.ForeignKey(WordCombination, related_name='sroown_managedeputyfull_set', verbose_name=u'ФИО заместителя руководителя постоянно действующего коллегиального органа управления СРО (полное)')
    signdeputy       = models.BooleanField(blank=False, default=False, verbose_name=u'Заместитель подписывает документы')

    tplprefix        = models.CharField(max_length=10, null=False, blank=False, verbose_name=u'Префикс шаблонов')
    ftp              = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'FTP')	# ftp host to upload
    path             = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Path')	# ftp path to upload
    sshhost	         = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'SSH host')
# to delete {   
    bosstitle        = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'Должность начальника')
    boss             = models.CharField(max_length=20, null=False, blank=False, verbose_name=u'ФИО заместителя руководителя постоянно действующего коллегиального органа управления СРО (краткое)')
# } to delete   


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/sro/view/%i/" % self.id

    def    asstr(self):
        return self.sro.name.asstr()

    def    __unicode__(self):
        return self.asstr()

#    def save(self, force_insert = False, force_update = False):
#        ExtraObject.save(self,force_insert, force_update)

    class    Meta:
        ordering = ('sro',)
        verbose_name = u'СРО.Своё'
        verbose_name_plural = u'СРО.Свои'


class    StageVer(models.Model):
    id        = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Наименование')

    def    __unicode__(self):
        return self.name

    class    Meta:
        ordering = ('id',)
        verbose_name = u'Версия видов работ'
        verbose_name_plural = u'Версии видов работ'


class    Stage(AL_Node):
    id        = models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
    ver        = models.ForeignKey(StageVer, null=False, blank=False, verbose_name=u'Версия')
    srotype        = models.ForeignKey(SroType, blank=False, verbose_name=u'Тип СРО')
    no        = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'№ п/п')
    code        = models.CharField(max_length=10, blank=False, verbose_name=u'Код')
    parent        = models.ForeignKey('self', related_name='children_set', null=True, blank=True, db_index=True, verbose_name=u'Предок')
    name        = models.CharField(max_length=255, blank=False, verbose_name=u'Наименование')
    isgroup        = models.BooleanField(blank=False, default=False, verbose_name=u'Группа')
    dangeronly    = models.BooleanField(blank=False, default=False, verbose_name=u'Только опасный')
    node_order_by    = ['id']

    def    asstr(self):
        return u'%s %s' % (self.code, self.name)

    def    __unicode__(self):
        return self.asstr()

    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"admin/sro2/stage/%i/" % self.id
    
    class    Meta:
        ordering = ('srotype', 'no',)
        verbose_name = u'Вид работ'
        verbose_name_plural = u'Виды работ'

class    EventType(models.Model):
    name        = models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
    comments    = models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        verbose_name = u'Тип события'
        verbose_name_plural = u'Типы событий'

class    Agent(models.Model):
    name        = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'Наименование')

    def    asstr(self):
        return self.name

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        verbose_name        = u'Агент'
        verbose_name_plural    = u'Агенты'


def    _csv_stages(stagelist, danger, sep=u'\n'):
    q = stagelist.permitstage_set.filter(danger=danger).order_by('stage__id',).values_list('stage__ver', 'stage__parent', 'stage__code', 'stage__name')
    subitems = list()
    field = u''
    for i in q:
        if (i[1]):
            subitems.append(i[2])
        else:
            if (subitems):
                field += (sep + ', '.join(subitems))
                subitems = list()
            field += (sep + i[2] + '. ' + i[3])
    if (subitems):
        field += (sep + ', '.join(subitems))
        subitems = list()
    return field


class    Protocol(ExtraObject,models.Model):
    sro        = models.ForeignKey(Sro, verbose_name=u'СРО')
    no        = models.CharField(max_length=30, null=False, blank=False, unique=False, verbose_name=u'Номер протокола')
    date        = models.DateField(null=False, blank=False, verbose_name=u'Дата протокола')
    type        = models.IntegerField(null=False, default=0, max_length=1, verbose_name=u'Тип протокола')    #

    def    __strdatedot(self,date):
        date = str(date).split('-')
        date ='%s.%s.%s' % (date[2], date[1], date[0])
        return date

    def    asstr(self):
        return u'%s (%s): № %s от %s' % (u'Протокол '+(u'ЗП', u'ДК', u'ОС')[self.type], self.sro.name, self.no,self.__strdatedot(self.date))

    def    asstr_short(self):
        return (u'Заседания Правления', u'Дисциплинарной Комиссии', u'Общего Собрания')[self.type]

    def    asstr_full(self):
        return u'%s %s: № %s от %s' % (u'Протокол ' + self.asstr_short(), self.sro.name, self.no,self.__strdatedot(self.date))

    def    __unicode__(self):
        return self.asstr()


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/protocol/%i/" % self.id
    class    Meta:
        ordering = ('sro', 'date', 'type')
        verbose_name        = u'Протокол'
        verbose_name_plural    = u'Протоколы'


class    Reason(models.Model):
    title = models.CharField(max_length=550, null=False, blank=False, verbose_name=u'Содержание')
    def    __unicode__(self):
        return self.title


class    OrgSro(ExtraObject,models.Model):
    org             = models.ForeignKey(Org, verbose_name=u'Организация')
    sro             = models.ForeignKey(Sro, verbose_name=u'СРО')
    regno           = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'Реестровый №')
    regdate         = models.DateField(null=True, blank=True, verbose_name=u'Дата членства в НП')
    paydate         = models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты взноса в КФ')
    paysum          = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Сумма взноса в КФ')
    paydatevv       = models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты вступительного взноса')
    comments        = models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
    publish         = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Публиковать')
    agent           = models.ForeignKey(Agent, null=True, blank=True, verbose_name=u'Агент')
    currperm        = models.ForeignKey('Permit', null=True, blank=True, verbose_name=u'Действующее разрешение', related_name='currperm_id')
    user            = models.ForeignKey(User, null=True, blank=True, verbose_name=u'Пользователь')
    events          = models.ManyToManyField(EventType, through='OrgEvent', verbose_name=u'События')
    speccase        = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Особый случай')
    speccomments    = models.TextField(null=True, blank=True, verbose_name=u'Особые коментарии')
    inprotocol      = models.ForeignKey(Protocol, null=True, blank=True, verbose_name=u'Протокол-основание принятия', related_name='inprotocol')    # FIXME: must be self sro only
    exprotocol      = models.ForeignKey(Protocol, null=True, blank=True, verbose_name=u'Протокол-основание исключения', related_name='exprotocol')    # FIXME: must be self sro only
    status          = models.IntegerField(null=False, default=0, max_length=1, verbose_name=u'Статус организации в СРО')    # 1: candidate, 2: member, 3: excluded
    caseno          = models.IntegerField(null=True, blank=True, verbose_name='Регистрационный Номер')
    reason          = models.ManyToManyField(Reason,through='OrgReason',null=True, blank=True, verbose_name=u'Причина исключения')
    excludedate     = models.DateField(null=True, blank=True, verbose_name=u'Дата исключения')
    aff         = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Аффилированность')

    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/orgsro/%i/" % self.id

    def    asstr(self):
        return u'%s (%s)' % (self.org.shortname,self.sro.name)

    def    __unicode__(self):
        return self.asstr()

    def test(self):
#        from mid import get_request
        return get_request()

    def    permits2str(self, sep=u'\n'):
        '''
        @return str: string of permits
        '''
        stages = u''
        currperm = False
        for stagelist in self.stagelist_set.instance_of(Permit).order_by('-permit__date'):
            if ((not currperm) and (self.currperm is not None) and (stagelist != self.currperm)):
                continue
            else:
                currperm = True
            if stages:
                stages += (sep + u'Ранее выданные:\n')
            stages += (u'Свидетельство № ' + stagelist.no + u' от ' + str(stagelist.date))
            if stagelist.protocol:
                stages += (u' (протокол № ' + stagelist.protocol.no  + ' от ' + str(stagelist.protocol.date) + ')')
            if (stagelist == self.currperm):
                stages += (u' - действующее')
            else:    # для старых свидетельств не печатаются перечни видов работ
                continue
            stages += (u':')
            stages += (sep + u'Перечень видов работ, которые оказывают влияние на безопасность объектов капитального строительства:')
            stages += _csv_stages(stagelist, False)
            if stagelist.permitstage_set.count_danger():
                stages += (sep + sep + u'Перечень видов работ, которые оказывют влияние на безопасность особо опасных, технически сложных и уникальных объектов:')
                stages += _csv_stages(stagelist, True)
        return stages

    class    Meta:
        ordering = ('org',)
        verbose_name        = u'Организация в СРО'
        verbose_name_plural    = u'Организации в СРО'
        #unique_together        = [('org', 'sro')]


class    OrgReason(models.Model):
    orgsro        = models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
    reason        = models.ForeignKey(Reason, verbose_name=u'Причина')


class    OrgEvent(models.Model):
    orgsro        = models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
    type        = models.ForeignKey(EventType, verbose_name=u'Типа события')
    date        = models.DateField(blank=False, verbose_name=u'Дата')
    comments    = models.CharField(max_length=100, blank=True, verbose_name=u'Коментарий')

    def    asstr(self):
        return u'%s: %s: %s' % (self.orgsro, self.date, self.type)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('orgsro', 'date')
        verbose_name        = u'Организация.СРО.Событие'
        verbose_name_plural    = u'Организация.СРО.События'


class    OrgLicense(ExtraObject,models.Model):
    orgsro        = models.OneToOneField(OrgSro, verbose_name=u'Организация.СРО')
    no        = models.CharField(null=False, blank=False, unique=True, max_length=100, verbose_name=u'Номер лицензии')    # unique=True
    datefrom    = models.DateField(null=False, blank=False, verbose_name=u'Выдана')
    datedue        = models.DateField(null=False, blank=False, verbose_name=u'Действительна до')

    def    asstr(self):
        return u'%s, до %s' % (self.no, self.datedue)

    def    __unicode__(self):
        return self.asstr()


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/orgsro/%i/" % self.id

    class    Meta:
        ordering = ('orgsro',)
        verbose_name = u'Организация.СРО.Лицензия'
        verbose_name_plural = u'Организация.СРО.Лицензии'


class    OrgInsurance(ExtraObject,models.Model):
    orgsro        = models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
    insurer        = models.ForeignKey(Insurer, null=False, blank=False, verbose_name=u'Страховщик')
    no        = models.CharField(null=False, blank=False, max_length=50, verbose_name=u'Номер договора')
    date        = models.DateField(null=False, blank=False, verbose_name=u'Дата договора')
    sum        = models.PositiveIntegerField(null=False, blank=False, verbose_name=u'Страховая сумма')
    datefrom    = models.DateField(null=True, blank=True, verbose_name=u'Страховка с')
    datedue        = models.DateField(null=True, blank=True, verbose_name=u'Страховка до')
    active         = models.BooleanField(null=False, blank=False, default=True, verbose_name=u'Действующая')


    def get_absolute_url(self):
        return self.orgsro.get_absolute_url()

    def    asstr(self):
        return u'%s от %s, %d руб, с %s по %s' % (self.no, strdatedot(self.date), self.sum, self.datefrom, self.datedue)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('orgsro',)
        verbose_name = u'Организация.Страховка'
        verbose_name_plural = u'Организация.Страховки'


class    StageListType(models.Model):
    id        = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
    name        = models.CharField(max_length=30, blank=False, unique=True, verbose_name=u'Наименование')

    def    asstr(self):
        return u'%d: %s' % (self.id, self.name)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        verbose_name        = u'ТипСпискаВидовРабот'
        verbose_name_plural    = u'ТипыСпискаВидовРабот'


class    StageList(PolymorphicModel):
    orgsro        = models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
    ver        = models.ForeignKey(StageVer, null=False, blank=False, verbose_name=u'Версия')
    publish        = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Публиковать')
    stages        = models.ManyToManyField(Stage, through='PermitStage', related_name='stages', verbose_name=u'Виды работ')


    def get_absolute_url(self):
        return LOGIN_REDIRECT_URL+"sro2/stagelist/%i/0/0/" % self.id

    def    __unicode__(self):
        return self.orgsro

    def    isperm(self):
        return False

    class    Meta:
        ordering = ('orgsro',)
        verbose_name        = u'СписокВидовРабот'
        verbose_name_plural    = u'СпискиВидовРабот'


class    PSManager(models.Manager):
    def    dict(self, danger):
        '''
        @param: danger
        return dict: 'Stage': children{}
        '''
        q = self.filter(danger=danger).order_by('stage__id',)
        retvalue = SortedDict()
        for i in q:
            stage = i.stage
            item = {'children': SortedDict(), 'paused': i.paused}
            if (stage.is_root()):    # level 0
                retvalue[stage] = item
            else:
                # retvalue[stage.parent][stage] = SortedDict()
                parent = stage.parent
                grandparent = parent.parent
                if (grandparent is None):    # level 1
                    retvalue[parent]['children'][stage] = item
                else:                # level 2
                    retvalue[grandparent]['children'][parent]['children'][stage] = item
        return retvalue

    def    dict_extra(self, stagelist, danger):
        '''
        danger, srotype, ver
        return dict: 'Stage': exists: bool, children{}
        '''
        q = self.filter(danger=danger).order_by('stage__id',)    # get permitstages
        tmp = SortedDict()
        for i in q:                        # convert to sorted dict {Stage: True,}
            tmp[i.stage] = i
        retvalue = SortedDict()
        if (danger):
            stages = Stage.objects.filter(ver=stagelist.ver, srotype=stagelist.orgsro.sro.type).order_by('id')
        else:
            stages = Stage.objects.filter(ver=stagelist.ver, srotype=stagelist.orgsro.sro.type, dangeronly=False).order_by('id')
        for stage in stages:    # fixme: danger
            if (tmp.has_key(stage)):
                paused = tmp[stage].paused
            else:
                paused = None
            item = {'exists': tmp.has_key(stage), 'children': SortedDict(), 'paused': paused}
            if (stage.is_root()):            # level 0
                retvalue[stage] = item
            else:
                parent = stage.parent
                grandparent = parent.parent
                if (grandparent is None):    # level 1
                    retvalue[parent]['children'][stage] = item
                else:                # level 2
                    retvalue[grandparent]['children'][parent]['children'][stage] = item
        return retvalue
    def    sorted(self):
        return self.all().order_by('stage__id',)
    def    list_ordinar(self):
        return self.filter(danger=False).order_by('stage__id',)
    def    list_danger(self):
        return self.filter(danger=True).order_by('stage__id',)
    def    count_ordinar(self):
        return self.filter(stage__isgroup = False, danger=False).count()
    def    count_danger(self):
        return self.filter(stage__isgroup = False, danger=True).count()


class    PermitStage(models.Model):
    stagelist    = models.ForeignKey(StageList, verbose_name=u'Список')
    stage        = models.ForeignKey(Stage, verbose_name=u'Вид работ')
    danger        = models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Опасный')
    paused        = models.DateField(null=True, blank=True, verbose_name=u'Приостановлено до')
    objects        = PSManager()

    def    asstr(self):
        return u'%s: %s' % (self.stagelist, self.stage)

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        verbose_name        = u'СписокВидовРабот.ВидРабот'
        verbose_name_plural    = u'СписокВидовРабот.ВидыРабот'
        unique_together        = [('stagelist', 'stage', 'danger'),]


class    Statement(ExtraObject,StageList):
    date        = models.DateField(null=True, blank=True, verbose_name=u'Дата Заявления')
    rejectprotocol      = models.ForeignKey(Protocol, null=True, blank=True, verbose_name=u'Протокол-отказ')    # FIXME: must be self sro only



    def    asstr(self):
        return u'%s. Заявление от %s' % (self.orgsro, strdatedot(self.date))

    def    id_str(self):
        return str(self.id)

    def    __unicode__(self):
        return u'Заявление от %s' % strdatedot(self.date)
    def    isperm(self):
        return False
    def isstatement(self):
        return True
    class    Meta:
        verbose_name        = u'Заявление'
        verbose_name_plural    = u'Заявления'


class Original(PolymorphicManager):
    def get_query_set(self):
        return super(Original, self).get_query_set().filter(status=0)


class Snaps(PolymorphicManager):
    def get_query_set(self):
        return super(Snaps, self).get_query_set().filter(status__gt=0)


class    Permit(ExtraObject,StageList):
    no        = models.CharField(max_length=50, null=False, blank=False, unique=False, verbose_name=u'Реестровый номер')
    date        = models.DateField(null=True, blank=True, verbose_name=u'Дата')
    datedue        = models.DateField(null=True, blank=True, verbose_name=u'Дата аннулирования')
    protocol    = models.ForeignKey(Protocol, null=True, blank=True, verbose_name=u'Протокол')    # FIXME: must be self sro only
    statement    = models.ForeignKey(Statement, null=True, blank=True, verbose_name=u'Заявление')
    status        = models.IntegerField(null=False, default=0, max_length=1, verbose_name=u'Статус свидетельства') # 0: new, 1: pause, 2: resume
    #original=Original(Permit)

    def    asstr(self):
        return u'%s. свидетельство № %s от %s' % (self.orgsro, self.no, strdatedot(self.date))


    def    asstr_snapstatus(self):
        return (u'Создание', u'Приостановка', u'Возобновление')[self.status]

    def    __unicode__(self):
        return u'Свидетельство № %s от %s' % (self.no, strdatedot(self.date))


    def    asstr_snapstatus2(self):
        if self.orgsro.currperm and self.no == self.orgsro.currperm.no:
            if self.status:
                return 'Действующее, %s' % (u'', u'Приостановлено', u'Возобновлено')[self.status]
            else:
                return 'Действующее'
        else:
            if self == Permit.objects.filter(orgsro=self.orgsro).order_by('-date')[0]:
                return 'Новое'
            else:
                return 'Заменено'

    def    isperm(self):
        return True

    def     isstatement(self):
        return False

    def    get_datetill(self):    # yet another crutch
        '''
        @return date - end date of pause
        '''
        retvalue = None
        if self.status == 1:
            retvalue = PermitStage.objects.filter(stagelist=self)[0].paused
        return retvalue

    def    get_daystill(self):    # yet another crutch
        '''
        @return int - days of pause
        '''
        retvalue = 0
        if self.status == 1:
            retvalue = (PermitStage.objects.filter(stagelist=self)[0].paused - self.date).days
        return retvalue

    def save(self, force_insert = False, force_update = False, action=''):
        if not self.status:
            ExtraObject.save(self,force_insert,force_update)
        else:
            ExtraObject.save(self,force_insert,force_update,4)

    class    Meta:
        verbose_name        = u'Свидетельство'
        verbose_name_plural    = u'Свидетельства'


class    AllienPermit(StageList):
    '''
    Свидетельство чужого СРО
    '''
    no        = models.CharField(max_length=50, null=False, blank=False, unique=False, verbose_name=u'Рег. №')
    date        = models.DateField(null=False, blank=False, verbose_name=u'Дата')
    protocol    = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'Протокол №')
    protodate    = models.DateField(null=False, blank=False, verbose_name=u'Дата протокола')

    def    __unicode__(self):
        return u'Чужое Свидетельство № %s от %s' % (self.no, self.date)

    class    Meta:
        verbose_name        = u'Свидетельство чужое'
        verbose_name_plural    = u'Свидетельства чужие'


class    PersonOrgSro(models.Model):
    person        = models.ForeignKey(Person, verbose_name=u'Человек')
    org        = models.ForeignKey(Org, verbose_name=u'Организация')
    sro        = models.ForeignKey(Sro, verbose_name=u'СРО')

    def    asstr(self):
        return u'%s: %s: %s' % (self.person.asstr(), self.org.asstr(), self.sro.asstr())

    def    __unicode__(self):
        return self.asstr()

    class    Meta:
        ordering = ('person',)
        verbose_name        = u'Человек.Организация.СРО'
        verbose_name_plural    = u'Человек.Организация.СРО'
        unique_together        = [('person', 'org', 'sro')]
