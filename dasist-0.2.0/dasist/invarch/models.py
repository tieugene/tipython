"""
invarch.models
"""

# 1. system
import json
# 2. django
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
# 4. local
from core.models import FileSeq
from contrib.models import Org


class Scan(models.Model):
    fileseq = models.OneToOneField(FileSeq, on_delete=models.CASCADE, primary_key=True, verbose_name='Файлы')
    place = models.CharField(max_length=24, db_index=True, verbose_name='Объект')    # max=22
    subject = models.CharField(max_length=32, null=True, blank=True, db_index=True, verbose_name='Подобъект')    # max = 28
    depart = models.CharField(max_length=16, null=True, blank=True, db_index=True, verbose_name='Направление')    # max=14    # max=
    # FIXME: null=False
    payer = models.CharField(max_length=16, null=True, blank=True, db_index=True, verbose_name='Плательщик')    # max=11
    # FIXME: null=False
    shipper = models.ForeignKey(Org, on_delete=models.CASCADE, null=True, blank=True, db_index=True, verbose_name='Поставщик')
    # FIXME: delete
    supplier = models.CharField(max_length=64, null=True, blank=True, db_index=True, verbose_name='Продавец')    # 48
    no = models.CharField(max_length=32, db_index=True, verbose_name='Номер')        # max=22
    date = models.DateField(db_index=True, verbose_name='Дата')
    # FIXME: null=False
    sum = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, db_index=True, verbose_name='Сумма')
    events = models.TextField(null=True, blank=True, verbose_name='История')

    def __unicode__(self):
        return str(self.pk)

    def decode_events(self):
        return json.loads(self.events) if self.events else list()

    class Meta:
        # unique_together    = (('invarch', 'type', 'name'),)
        ordering = ('fileseq',)
        verbose_name = 'Скан'
        verbose_name_plural = 'Сканы'


@receiver(post_delete, sender=Scan)
def _scan_delete(sender, instance, **kwargs):
    instance.fileseq.delete()


class Event(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, db_index=True, verbose_name='Скан')
    approve = models.CharField(max_length=64, db_index=True, verbose_name='Подписант')    # max=61
    resume = models.BooleanField(db_index=True, verbose_name='Резолюция')
    ctime = models.DateTimeField(db_index=True, verbose_name='ДатаВремя')
    comment = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name='Камменты')    # max=260

    def get_approve_lname(self):
        return self.approve.split(' ', 1)[0]

    def __unicode__(self):
        return '%s: %s' % (self.approve, self.comment)

    class Meta:
        ordering = ('ctime',)
        verbose_name = 'Резолюция'
        verbose_name_plural = 'Резолюции'
