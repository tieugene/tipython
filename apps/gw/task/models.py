# -*- coding: utf-8 -*-

'''
lansite.gw.task.models.py

Multitask: subtasks w/o subj, desk, etc - just assignee, state
'''

from django.db import models

from datetime import datetime

from gw.bits.models import *

class	Task(Object):
	author		= models.ForeignKey(GwUser, null=False, blank=False, verbose_name=u'Автор')
	created		= models.DateTimeField(null=False, blank=False, default=datetime.now, verbose_name=u'Создана')
	deadline	= models.DateField(null=True, blank=True, verbose_name=u'Завершить до')
	subject		= models.CharField(max_length=128, null=False, blank=False, verbose_name=u'Тема')
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')
	done		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Завершено')

	def	asstr(self):
		return self.subject

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Задача'
		verbose_name_plural = u'Задачи'

class	ToDoCat(models.Model):
	author		= models.ForeignKey(GwUser, null=False, blank=False, verbose_name=u'Автор')
	name		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('name',)
		verbose_name		= u'ToDo.Категория'
		verbose_name_plural	= u'ToDo.Категории'

class	ToDo(Task):
	category	= models.ForeignKey(ToDoCat, null=True, blank=True, verbose_name=u'Категория')

	def	getclassname(self):
		return 'ToDo'

	def	getclassid(self):
		return 1

	class	Meta:
		app_label = 'gw'
		verbose_name = u'ToDo'
		verbose_name_plural = u'ToDo'

class	AssignCat(models.Model):
	name		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Наименование')
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('name',)
		verbose_name		= u'Задание.Категория'
		verbose_name_plural	= u'Задания.Категории'

class	Assign(Task):
	'''
	comments
	files
	DependsOn - tasks not sons
	'''
	assignee	= models.ForeignKey(GwUser, null=False, blank=False, related_name='assignee_id', verbose_name=u'Исполнитель')
	importance	= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Важность')
	read		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Прочтено')
	category	= models.ForeignKey(AssignCat, null=True, blank=True, verbose_name=u'Категория')

	def	getclassname(self):
		return 'Assign'

	def	getclassid(self):
		return 2

	def	cantbeclosed(self):
		#return self.child.all().count()		# .objects.filter(read).count()
		#return self.child.filter(done=False)	# .objects.filter(read).count()
		#return SubObject.objects.filter(done=False)
		#return Assign.objects.filter(master=self, done=False, read=False).count()
		return True

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Задание'
		verbose_name_plural = u'Задания'

# class	Appointment (iCalendar/Meeting)
# class	Event (iEvent)
