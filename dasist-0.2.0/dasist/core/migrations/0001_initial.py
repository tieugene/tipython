# Generated by Django 3.2.7 on 2021-09-13 17:31

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.my_upload_to, verbose_name='Файл')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Имя файла')),
                ('mime', models.CharField(db_index=True, max_length=16, verbose_name='Тип Mime')),
                ('ctime', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Записано')),
                ('size', models.PositiveIntegerField(db_index=True, verbose_name='Размер')),
                ('md5', models.CharField(db_index=True, max_length=32, verbose_name='MD5')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='FileSeq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Последовательность файлов',
                'verbose_name_plural': 'Последовательности файлов',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.CharField(max_length=12, unique=True, verbose_name='VAP')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Short name')),
                ('fullname', models.CharField(db_index=True, max_length=64, verbose_name='Full name')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='FileSeqItem',
            fields=[
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.file', verbose_name='File')),
                ('order', models.PositiveSmallIntegerField(db_index=True, verbose_name='#')),
                ('fileseq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fileseq', verbose_name='File sequence')),
            ],
            options={
                'verbose_name': 'Файл последовательности',
                'verbose_name_plural': 'Файлы последовательности',
                'ordering': ('file', 'order'),
            },
        ),
        migrations.AddField(
            model_name='fileseq',
            name='files',
            field=models.ManyToManyField(through='core.FileSeqItem', to='core.File', verbose_name='Файлы'),
        ),
    ]
