"""
contract.models
"""

# 2. django
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
# 3. local
from core.models import FileSeq
from contrib.models import Org, State, Role, Approver, Place, Subject, Department, Payer, Customer
from invoice.views_extras import ROLE_ACCOUNTER, ROLE_CHIEF


class Contract(models.Model):
    fileseq = models.OneToOneField(FileSeq, on_delete=models.CASCADE, primary_key=True, verbose_name='Файлы')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_contracts', db_index=True, verbose_name='Объект')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_contracts', null=True, blank=True, db_index=True, verbose_name='ПодОбъект')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_contracts', null=True, blank=True, db_index=True, verbose_name='Заказчик')
    depart = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_contracts', null=True, blank=True, db_index=True, verbose_name='Направление')
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, related_name='payer_contracts', db_index=True, verbose_name='Наша фирма')
    shipper = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='shipper_contracts', db_index=True, verbose_name='Контрагент')
    assign = models.ForeignKey(Approver, on_delete=models.CASCADE, related_name='assigned_contracts', db_index=True, verbose_name='Исполнитель')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_contracts', db_index=True, verbose_name='Состояние')
    doc_no = models.CharField(max_length=32, db_index=True, verbose_name='Номер договора')    # max=11
    doc_date = models.DateField(db_index=True, verbose_name='Дата договора')
    doc_sum = models.DecimalField(max_digits=11, decimal_places=2, null=True, db_index=True, verbose_name='Сумма договора')

    def __str__(self):
        return str(self.pk)

    def set_state_id(self, pk):
        self.state = State.objects.get(pk=pk)

    def get_state_id(self):
        return self.state.pk

    def get_state_name(self):
        return self.state.name

    def get_state_color(self):
        return self.state.color

    def get_mgr(self):
        return self.route_set.get(role=ROLE_CHIEF)

    def get_booker(self):
        return self.route_set.get(role=ROLE_ACCOUNTER)

    def get_is_signatory(self, approver):
        return self.route_set.get(approve=approver)

    class Meta:
        db_table = 'contract'
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'


@receiver(post_delete, sender=Contract)
def _contract_delete(sender, instance, **kwargs):
    instance.fileseq.delete()


class Route(models.Model):
    doc = models.ForeignKey(Contract, on_delete=models.CASCADE, db_index=True, verbose_name='Договор')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', db_index=True, verbose_name='Роль')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, related_name='+', db_index=True, verbose_name='Подписант')
    done = models.BooleanField(db_index=True, default=False, verbose_name='Согласовано')

    def __str__(self):
        return '%d: %s: %d' % (self.contract.pk, self.approve.get_fio() if self.approve else self.role.name, int(self.done))

    def get_str(self):
        return self.approve.get_fio() if self.approve else self.role.name

    class Meta:
        unique_together = ('contract', 'role')
        ordering = ('contract',)
        verbose_name = 'Подписант'
        verbose_name_plural = 'Подписанты'


class Event(models.Model):
    doc = models.ForeignKey(Contract, on_delete=models.CASCADE, db_index=True, verbose_name='Договор')
    ctime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='ДатаВремя')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, related_name='+', db_index=True, verbose_name='Подписант')
    comment = models.TextField(null=True, blank=True, verbose_name='Камменты')

    def __str__(self):
        return '%s: %s' % (self.approve, self.comment)

    class Meta:
        ordering = ('ctime',)
        verbose_name = 'Резолюция'
        verbose_name_plural = 'Резолюции'
