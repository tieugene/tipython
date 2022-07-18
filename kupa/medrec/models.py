# -*- coding: utf-8 -*-
'''
Workflow:
* Change your models (in models.py).
* Run python manage.py makemigrations to create migrations for those changes
* Run python manage.py migrate to apply those changes to the database.


'''

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver

import os

class	Client(models.Model):
	'''
	TODO:
	- кто кому рабинович
	- почему рабинович
	'''
	# ? User
	lname	= models.CharField(max_length=32, null=True, blank=True, verbose_name=u'Ф')
	fname	= models.CharField(max_length=32, null=True, blank=True, verbose_name=u'И')
	mname	= models.CharField(max_length=32, null=True, blank=True, verbose_name=u'О')
	price	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Цена')	# < comments
	gender	= models.BooleanField(verbose_name=u'Пол')
	birth	= models.DateField(null=True, blank=True, verbose_name=u'День рождения')
	phone1	= models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Телефон №1')
	phone2	= models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Телефон №2')
	warning	= models.BooleanField(verbose_name=u'Внимание!')
	comment	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Камменты')		# < ФИО
	details	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')
	# virtual: photos
	# 2 del
	user	= models.ForeignKey(User, null=True, verbose_name=u'Пользователь')
	name	= models.CharField(max_length=160, null=True, blank=True, verbose_name=u'ФИО')
	birthday = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'День Рожденья')
	new	= models.NullBooleanField(verbose_name=u'Новый')
	invidate= models.DateField(null=True, blank=True, verbose_name=u'Дата приглашения')
	invidesc= models.CharField(max_length=80, null=True, blank=True, verbose_name=u'Описание приглашения')
	# возраст == 0
	# Дата SMS
	# Текст SMS

	def	get_fio(self):
		return "%s %s %s" % (self.lname, self.fname, self.mname)

	def	__unicode__(self):
		return self.get_fio()

	def	get_gender(self):
		return 'М' if self.gender else 'Ж'

	def	get_warning(self):
		return '!' if self.warning else '-'

	def	get_new(self):
		return '+' if self.warning else '-'

	def	get_img_rpath(self):
		return '%04d' % self.pk

	def	get_img_dir(self):
		return os.path.join(settings.MEDIA_ROOT, self.get_img_rpath())

	def	get_img_path(self, img):
		return os.path.join(self.get_img_dir(), img)

	def	get_img_list(self):
		retvalue = list()
		dir = self.get_img_dir()
		if (os.path.exists(dir) and os.path.isdir(dir)):
			retvalue = os.listdir(dir)
			retvalue.sort()
		return retvalue

	def	del_img(self, img):
		fn = self.get_img_path(img)
		if (os.path.exists(fn) and os.path.isfile(fn)):
			os.unlink(fn)
			dir = self.get_img_dir()
			if not (self.get_img_list()):
				os.rmdir(dir)

	def	img_add(self, img):
		dir = self.get_img_dir()
		if not os.path.exists(dir):
			os.mkdir(dir)
		fn = self.get_img_path(img.name)
		with open(fn, 'wb+') as destination:
			for chunk in img.chunks():
				destination.write(chunk)

	class   Meta:
		#unique_together		= (('name',),)
		ordering                = ('lname', 'fname', 'mname', 'comment')
		verbose_name            = u'Клиент'
		verbose_name_plural     = u'Клиенты'

@receiver(pre_delete, sender=Client)
def	_client_delete(sender, instance, **kwargs):
	for i in instance.get_img_list():
		instance.del_img(i)

duration = ('0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00')

class	Record(models.Model):
	user	= models.ForeignKey(User, verbose_name=u'Пользователь')
	client	= models.ForeignKey(Client, verbose_name=u'Клиент')
	date	= models.DateField(verbose_name=u'Дата')
	time	= models.TimeField(verbose_name=u'Время')				# 08:00..22:00
	durat	= models.PositiveSmallIntegerField(verbose_name=u'Длительность')	# 0..7
	comment	= models.CharField(max_length=160, null=True, blank=True, verbose_name=u'Камменты')
	medrec	= models.TextField(null=True, blank=True, verbose_name=u'Запись медкарты')
	# 2 del
	code	= models.PositiveIntegerField(verbose_name=u'Код')			# 1..39
	state	= models.PositiveSmallIntegerField(verbose_name=u'Состояние')		# 0, 1, 10, 11

	def	__unicode__(self):
		return "%s %s: %s" % (self.date, self.time, self.client.get_fio())

	def	get_durat(self):
		return duration[self.durat]

	def	get_yymmdd(self):
		return self.date.strftime("%y%m%d")

	class   Meta:
		unique_together		= (('user', 'date', 'time'),)
		ordering                = ('date', 'time')
		verbose_name            = u'Посещение'
		verbose_name_plural     = u'Посещения'

#class	Image(models.Model):
#	user	= models.ForeignKey(User, verbose_name=u'Пользователь')
#	image	= ImageField(upload_to=...)
