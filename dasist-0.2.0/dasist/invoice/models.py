"""
invoice.models

TODO: tune on_delete
"""
# 2. django
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
# 4. local
from core.models import FileSeq
from contrib.models import Org, State, Role, Approver, Bank

ORD_MGR = 2
ORD_BOSS = 4


class Invoice(models.Model):
    fileseq = models.OneToOneField(FileSeq, on_delete=models.CASCADE, primary_key=True, verbose_name='Файлы')
    # TODO: contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_invoices', null=False, db_index=True, verbose_name='Договор')
    # TODO: bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_invoices', null=False, db_index=True, verbose_name='Банк')
    # DEL: place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_bills', null=False, blank=False, db_index=True, verbose_name='Объект')
    # DEL: subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_bills', null=True, blank=True, db_index=True, verbose_name='ПодОбъект')
    # DEL: depart = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_bills', null=True, blank=True, db_index=True, verbose_name='Направление')
    # DEL: payer = models.ForeignKey(Payer, on_delete=models.CASCADE, related_name='payer_bills', null=False, blank=False, db_index=True, verbose_name='Плательщик')
    shipper = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='shipper_invoices', null=False, blank=False, db_index=True, verbose_name='Поставщик')
    doc_no = models.CharField(max_length=32, db_index=True, verbose_name='Номер счета')    # max=11
    doc_date = models.DateField(db_index=True, verbose_name='Дата счета')
    doc_sum = models.DecimalField(max_digits=11, decimal_places=2, db_index=True, verbose_name='Сумма счета')
    sum_payed = models.DecimalField(max_digits=11, decimal_places=2, db_index=True, verbose_name='Оплачено')
    sum_2pay = models.DecimalField(max_digits=11, decimal_places=2, db_index=True, verbose_name='К оплате')
    assign = models.ForeignKey(Approver, on_delete=models.CASCADE, related_name='assigned_invoices', db_index=True, verbose_name='Исполнитель')
    rpoint = models.ForeignKey('Route', on_delete=models.CASCADE, null=True, related_name='rinvoice', db_index=True, verbose_name='Точка маршрута')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_invoices', db_index=True, verbose_name='Состояние')
    locked = models.BooleanField(null=False, blank=False, default=False, db_index=True, verbose_name='В работе')

    def __str__(self):
        return str(self.pk)

    def set_state_id(self, pk):
        self.state = State.objects.get(pk=pk)

    def get_state_id(self):
        return self.state.pk

    def get_state_name(self):
        return self.state.name

    def get_state_color(self):
        if (self.state.pk == 5) and self.locked:    # FIXME: hardcoded color
            return 'Aquamarine'
        else:
            return self.state.color

    def get_mgr(self):
        return self.route_set.get(order=ORD_MGR)

    def get_boss(self):
        return self.route_set.get(order=ORD_BOSS)

    class Meta:
        db_table = 'invoice'
        unique_together = (('shipper', 'doc_no', 'doc_date'),)
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'


@receiver(post_delete, sender=Invoice)
def _invoice_delete(sender, instance, **kwargs):
    instance.fileseq.delete()


class Route(models.Model):
    doc = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_index=True, verbose_name='Счет')
    # 1-based route point (assignee excluded)
    order = models.PositiveSmallIntegerField(db_index=True, verbose_name='#')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True, verbose_name='Роль')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, null=True, blank=True, db_index=True, verbose_name='Подписант')

    def __str__(self):
        return '%d.%d: %s' % (self.bill.pk, self.order, self.approve.get_fio() if self.approve else self.role.name)

    def get_str(self):
        return self.approve.get_fio() if self.approve else self.role.name

    class Meta:
        unique_together = (('invoice', 'order',), ('invoice', 'role'))
        ordering = ('invoice', 'order',)
        verbose_name = 'Точка маршрута'
        verbose_name_plural = 'Точки маршрута'


class Event(models.Model):
    doc = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_index=True, verbose_name='Счет')
    ctime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='ДатаВремя')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, db_index=True, verbose_name='Подписант')
    resume = models.BooleanField(db_index=True, verbose_name='Резолюция')
    comment = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name='Камменты')  # max=107

    def __str__(self):
        return '%s: %s' % (self.approve, self.comment)

    class Meta:
        ordering = ('ctime',)
        verbose_name = 'Резолюция'
        verbose_name_plural = 'Резолюции'
