from django.db import models
from invoice.models import Approver, Role


class RouteTemplate(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'#')
    name = models.CharField(max_length=32, verbose_name=u'Наименование')
    approvers = models.ManyToManyField(Approver, null=True, blank=True, related_name='acl', through='RouteTemplateACL',
                                       verbose_name='Подписанты')

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name',)
        ordering = ('id',)
        verbose_name = 'Шаблон маршрута'
        verbose_name_plural = 'Шаблоны маршрутов'


class RouteTemplateItem(models.Model):
    tpl = models.ForeignKey(RouteTemplate, on_delete=models.CASCADE, verbose_name='Шаблон маршрута')
    order = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='#')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Роль')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Подписант')
    areq = models.BooleanField(verbose_name='Требует Подписанта')

    def __unicode__(self):
        return '$%s #%d' % (self.tpl, self.order)

    class Meta:
        unique_together = (('tpl', 'order'),)
        ordering = ('tpl', 'order')
        verbose_name = 'Точка шаблона маршрута'
        verbose_name_plural = 'Точки шаблонов маршрутов'


class RouteTemplateACL(models.Model):
    tpl = models.ForeignKey(RouteTemplate, on_delete=models.CASCADE, verbose_name=u'Шаблон маршрута')
    approve = models.ForeignKey(Approver, on_delete=models.CASCADE, verbose_name=u'Подписант')

    class Meta:
        unique_together = (('tpl', 'approve'),)
        ordering = ('pk',)
        verbose_name = u'Права на маршрут'
        verbose_name_plural = u'Права на маршруты'
