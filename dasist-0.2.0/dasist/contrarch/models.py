# -*- coding: utf-8 -*-
"""
contrarch.models
"""

# 1. system
# 2. django
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
# 4. local
from core.models import FileSeq
from contrib.models import Org


class Contrarch(models.Model):
    fileseq = models.OneToOneField(FileSeq, on_delete=models.CASCADE, primary_key=True, verbose_name='Файлы')
    place = models.CharField(max_length=24, db_index=True, verbose_name='Объект')
    subject = models.CharField(max_length=32, null=True, blank=True, db_index=True, verbose_name='Подобъект')    # max = 28
    customer = models.CharField(max_length=8, null=True, blank=True, db_index=True, verbose_name='Заказчик')
    depart = models.CharField(max_length=16, null=True, blank=True, db_index=True, verbose_name='Направление')    # max=14    # max=
    payer = models.CharField(max_length=16, db_index=True, verbose_name='Плательщик')
    shipper = models.ForeignKey(Org, on_delete=models.CASCADE, db_index=True, verbose_name='Поставщик')
    docno = models.CharField(max_length=32, db_index=True, verbose_name='Номер')
    docdate = models.DateField(db_index=True, verbose_name='Дата')
    docsum = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, db_index=True, verbose_name='Сумма')
    # events = models.TextField(null=True, blank=True, verbose_name='История')

    def __unicode__(self):
        return str(self.pk)

    # def decode_events(self):
    #    return json.loads(self.events) if self.events else list()

    class Meta:
        # unique_together    = (('invarch', 'type', 'name'),)
        ordering = ('fileseq',)
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'


@receiver(post_delete, sender=Contrarch)
def _contrarch_delete(sender, instance, **kwargs):
    instance.fileseq.delete()


class Event(models.Model):
    contrarch = models.ForeignKey(Contrarch, on_delete=models.CASCADE, db_index=True, verbose_name='Договор')
    ctime = models.DateTimeField(db_index=True, verbose_name='ДатаВремя')
    approve = models.CharField(max_length=64, db_index=True, verbose_name='Подписант')
    comment = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name='Замечание')

    def get_approve_lname(self):
        return self.approve.split(' ', 1)[0]

    def __unicode__(self):
        return '%s: %s' % (self.approve, self.comment)

    class Meta:
        ordering = ('ctime',)
        verbose_name = 'Резолюция'
        verbose_name_plural = 'Резолюции'
