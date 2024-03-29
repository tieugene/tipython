# Generated by Django 3.2.7 on 2021-09-13 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('contrib', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('fileseq', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.fileseq', verbose_name='Файлы')),
                ('billno', models.CharField(db_index=True, max_length=32, verbose_name='Номер счета')),
                ('billdate', models.DateField(db_index=True, verbose_name='Дата счета')),
                ('billsum', models.DecimalField(db_index=True, decimal_places=2, max_digits=11, verbose_name='Сумма счета')),
                ('payedsum', models.DecimalField(db_index=True, decimal_places=2, max_digits=11, verbose_name='Оплачено')),
                ('topaysum', models.DecimalField(db_index=True, decimal_places=2, max_digits=11, verbose_name='Сумма к оплате')),
                ('locked', models.BooleanField(db_index=True, default=False, verbose_name='В работе')),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_bills', to='contrib.approver', verbose_name='Исполнитель')),
                ('depart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_bills', to='contrib.department', verbose_name='Направление')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_bills', to='contrib.payer', verbose_name='Плательщик')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_bills', to='contrib.place', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(db_index=True, verbose_name='#')),
                ('approve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contrib.approver', verbose_name='Подписант')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice', verbose_name='Счет')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contrib.role', verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'Точка маршрута',
                'verbose_name_plural': 'Точки маршрута',
                'db_table': 'invoice',
                'ordering': ('bill', 'order'),
                'unique_together': {('bill', 'order'), ('bill', 'role')},
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='rpoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rbill', to='invoice.route', verbose_name='Точка маршрута'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shipper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipper_bills', to='core.org', verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_bills', to='contrib.state', verbose_name='Состояние'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_bills', to='contrib.subject', verbose_name='ПодОбъект'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.BooleanField(db_index=True, verbose_name='Резолюция')),
                ('ctime', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='ДатаВремя')),
                ('comment', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Камменты')),
                ('approve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contrib.approver', verbose_name='Подписант')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice', verbose_name='Счет')),
            ],
            options={
                'verbose_name': 'Резолюция',
                'verbose_name_plural': 'Резолюции',
                'ordering': ('ctime',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together={('shipper', 'billno', 'billdate')},
        ),
    ]
