from django.db import models
from django.contrib.auth.models import User

STATE_ICON = (
    'pencil.svg',           # Edit
    'paper-plane-o.svg',    # OnWay
    'ban.svg',              # unlike
    'usd.svg',              # ?
    'check.svg',            # liked
    'archive.svg',          # put 2 archieve
)


class Org(models.Model):
    inn = models.CharField(null=False, blank=False, unique=True, max_length=12, verbose_name='VAP')
    name = models.CharField(null=False, blank=False, unique=True, max_length=40, verbose_name='Short name')  # max=38
    fullname = models.CharField(null=False, blank=False, db_index=True, max_length=64, verbose_name='Full name')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class State(models.Model):
    """
    Predefined states:
    1 - Черновик
    2 - В пути (на подписи у Подписантов)
    3 - Завернут (Счет: любым Подписантом; Договор: Юристом)
    4 - Оплачивается (Договор: 1. "Все дали добро, только таможня тормозит", 2. "таможня (юрист) дает добро")
    5 - Исполнен (Договор: 1. таможня дала добро; 2. Договор на базе)
    """
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='#')
    name = models.CharField(max_length=16, db_index=True, unique=True, verbose_name='Наименование')
    color = models.CharField(max_length=16, db_index=True, verbose_name='Цвет')
    # icon    = models.CharField(max_length=16, blank-True, null=True, verbose_name='Пиктограмма')

    def __str__(self):
        return self.name

    def get_icon(self):
        return STATE_ICON[self.id - 1]

    class Meta:
        ordering = ('id', )
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'


class Role(models.Model):
    """
    Predefined roles
    TODO: m2m user [via Approver]
    """
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='#')
    name = models.CharField(max_length=32, db_index=True, unique=True, verbose_name='Наименование')    # max=20
    # users        = models.ManyToManyField(User, null=True, blank=True, related_name='history', through='Approver', verbose_name='Подписанты')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class Approver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Пользователь')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True, verbose_name='Роль')
    jobtit = models.CharField(max_length=32, db_index=True, verbose_name='Должность')    # max=28
    canadd = models.BooleanField(db_index=True, verbose_name='Может создавать')

    class Meta:
        unique_together = (('role', 'user'),)
        ordering = ('role', 'user')
        verbose_name = 'Подписант'
        verbose_name_plural = 'Подписанты'

    def get_fio(self):
        """
        Varinats:
        * last_name > last_name
        * last_name first_name > last_name first_name[0].'.'
        * last_name first_name+middle_name
        """
        fname = self.user.first_name
        if fname:
            io = fname.split(' ', 2)
            if len(io) > 1:
                fio = '%s %s. %s.' % (self.user.last_name, io[0][0], io[1][0])
            else:
                fio = '%s %s.' % (self.user.last_name, io[0][0])
        else:
            fio = self.user.last_name
        return fio

    def __str__(self):
        return '%s %s (%s, %s)' % (
            self.user.last_name,
            self.user.first_name if self.user.first_name else '',
            self.jobtit,
            self.role.name
        )


class Place(models.Model):
    name = models.CharField(max_length=24, db_index=True, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Subject(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, db_index=True, related_name='subjects', verbose_name='Объект')
    name = models.CharField(max_length=32, db_index=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('place', 'name',),)
        ordering = ('place', 'id', )
        verbose_name = 'ПодОбъект'
        verbose_name_plural = 'ПодОбъект'


class Department(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='#')
    name = models.CharField(max_length=16, db_index=True, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Payer(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='#')
    name = models.CharField(max_length=16, db_index=True, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )
        verbose_name = 'Плательщик'
        verbose_name_plural = 'Плательщики'


class Customer(models.Model):
    """
    Заказчик
    """
    name = models.CharField(max_length=8, unique=True, db_index=True, verbose_name='Заказчик')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Bank(models.Model):
    name = models.CharField(max_length=8, unique=True, db_index=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
