# -*- coding: utf-8 -*-

'''
lansite.apps.task.models

Multitask: subtasks w/o subj, desk, etc - just assignee, state
'''

from django.db import models
from django.contrib.contenttypes.models import ContentType

from datetime import datetime

from apps.core.models import *

import objectpermissions
permissions = ['view', 'add', 'change', 'delete', 'chmod']

VTODO_STATUS_CHOICES = (
	(1, 'Needs-Action'),
	(2, 'In-Process'),
	(3, 'Completed'),
	(4, 'Cancelled'),
)

PRIORITY_CHOICES = (
	(1, 'High'),
	(5, 'Medium'),
	(9, 'Low'),
)
'''	Or:
	1	Max
	2	Above high
	3	High
	4	Below high
	5	Normal
	9	Min
'''

RESTRICTION_CHOICES = (
	(1, 'Public'),
	(2, 'Private'),
	(3, 'Confidential'),
	(4, 'Restricted'),
)

VTODO_STATUS_DICT = dict()	# idx => name
VTODO_STATUS_REVERSE = dict()	# name => idx
PRIORITY_DICT = dict()
PRIORITY_REVERSE = dict()
RESTRICTION_DICT = dict()
RESTRICTION_REVERSE = dict()

for i, j in VTODO_STATUS_CHOICES:
	VTODO_STATUS_DICT[i] = j
	VTODO_STATUS_REVERSE[j.upper()] = i

for i, j in PRIORITY_CHOICES:
	PRIORITY_DICT[i] = j
	PRIORITY_REVERSE[j.upper()] = i

for i, j in RESTRICTION_CHOICES:
	RESTRICTION_DICT[i] = j
	RESTRICTION_REVERSE[j.upper()] = i

class	Category(models.Model):
	'''
	user not Null - for current user only
	app not Null - for current model only
	name
	'''
	name		= models.CharField(max_length=32, null=False, blank=False, db_index=True, verbose_name=u'Наименование')
	user		= models.ForeignKey(User, null=True, blank=True, db_index=True, verbose_name=u'Автор')
	app		= models.ForeignKey(ContentType, null=True, blank=True, db_index=True, verbose_name=u'Приложение')
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')

	def	__unicode__(self):
		return self.name

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Категория'
		verbose_name_plural = u'Категории'
		ordering	= ('name', 'app', 'user')
		unique_together = (('name', 'user', 'app'),)

objectpermissions.register(Category, permissions)

class	Task(Object):
	'''
	Common parent for all tasks
	created - by History model
	Status:
		ToDo (was):	done:bool (New/Done)
		Assign (was):	done:bool x read:bool = New/Accepted/Done/Approved
		iCal vToDo:	Needs-Action/In-Progress/Completed/Cancelled
		iCal vEvent:	Tentative/Confirmed/Cancelled
		iCal vJournal:	Draft/Final/Canceled
	Restriction:
		Private:	None of the calendar data is visible.
		Public:		All of the calendar data is visible.
		Confidential:	Only start and end time of each instance is visible.
		Restricted:	Only start and end time, summary and location of each instance is visible.
	'''
	user		= models.ForeignKey(User, null=False, blank=False, verbose_name=u'Автор')
	categories	= models.ManyToManyField(Category, null=True, blank=True, through='TaskCat', verbose_name=u'Категории')

	def	__unicode__(self):
		return "task"

	def	getcategories(self):
		'''
		'''
		return ', '.join(self.taskcat_set.all().values_list('cat__name', flat=True))

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Задача'
		verbose_name_plural	= u'Задачи'

class	TaskAbstract(models.Model):
	created         = models.DateTimeField(null=False, blank=False, default=datetime.now, verbose_name=u'Создано')
	updated         = models.DateTimeField(null=False, blank=False, default=datetime.now, verbose_name=u'Изменено')
	summary		= models.CharField(max_length=128, null=False, blank=False, verbose_name=u'Тема')
	status		= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Состояние', choices=VTODO_STATUS_CHOICES)
	restriction	= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Видимость', choices=RESTRICTION_CHOICES)

	def	__unicode__(self):
		return self.summary

	def	getstatusname(self):
		'''
		FIXME: move to vTodo
		'''
		return VTODO_STATUS_DICT.get(self.status, None)

	def	getrestrictionname(self):
		return RESTRICTION_DICT.get(self.restriction, None)

	class	Meta:
		abstract = True

class	TaskCat(models.Model):
	task		= models.ForeignKey(Task, null=False, blank=False, verbose_name=u'Задача')
	cat		= models.ForeignKey(Category, null=False, blank=False, verbose_name=u'Категория')

	def	__unicode__(self):
		return u'%s: %s' % (self.cat.name, self)

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Категория задачи'
		verbose_name_plural	= u'Категории задач'
		unique_together = (('task', 'cat',),)

class	vCalAbstract(models.Model):
	'''
	RFC 5545 (iCalendar) parent
	FIXME: UUID not Null
	'''
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')
	start_d		= models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Начало (дата)')
	start_t		= models.TimeField(null=True, blank=True, db_index=True, verbose_name=u'Начало (время)')
	duration_d	= models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Длительность (Дни)')
	duration_t	= models.TimeField(null=True, blank=True, db_index=True, verbose_name=u'Длительность (Ч:М:С)')
	location	= models.CharField(max_length=64, null=True, blank=True, db_index=True, verbose_name=u'Место')
	priority	= models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Приоритет', choices=PRIORITY_CHOICES)
	URL		= models.URLField(null=True, blank=True, db_index=True, verbose_name=u'URL')
	attendee	= models.ForeignKey(User, null=True, blank=True, db_index=True, verbose_name=u'Участник')

	def	getclassname(self):
		return 'vCal'

	def	getclassid(self):
		return 2

	def	getpriorityname(self):
		return PRIORITY_DICT.get(self.priority, None)

	#def	tojson(self):
	#	return

	class	Meta:
		abstract = True

#class	vToDo(Logged, vCalAbstract):
class	vToDo(Task, TaskAbstract, vCalAbstract):
	due_d		= models.DateField(null=True, blank=True, db_index=True, verbose_name=u'До (дата)')
	due_t		= models.TimeField(null=True, blank=True, db_index=True, verbose_name=u'До (время)')
	completed	= models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Завершено')	# FIXME: vEvent too
	percent		= models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Процент')

	#def	__init__(self, *args, **kwargs):
	#	super(vCal, self).__init__(*args, **kwargs)
	#	status	= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Состояние', choices=VTODO_STATUS_CHOICES)

	def	getclassname(self):
		return 'vToDo'

	def	getclassid(self):
		return 3

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.task.views.todo_detail', [str(self.id)])

	def	get_edit_url(self):
		return ('apps.task.views.todo_edit', [str(self.id)])

	def	get_del_url(self):
		return ('apps.task.views.todo_del', [str(self.id)])

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Задача ToDo'
		verbose_name_plural = u'Задачи ToDo'
		permissions = (
			("read_vtodo", "Can read Задача ToDo"),
			("chmod_vtodo", "Can chmod Задача ToDo"),
		)

objectpermissions.register(vToDo, permissions)

class	vEvent(Task, Logged, TaskAbstract, vCalAbstract):
	'''
	comments
	files
	DependsOn - tasks not sons
	'''
	end_d		= models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Окончание (дата)')
	end_t		= models.TimeField(null=True, blank=True, db_index=True, verbose_name=u'Окончание (время)')

	def	getclassname(self):
		return 'vEvent'

	def	getclassid(self):
		return 4

	def	cantbeclosed(self):
		#return self.child.all().count()		# .objects.filter(read).count()
		#return self.child.filter(done=False)	# .objects.filter(read).count()
		#return SubObject.objects.filter(done=False)
		#return Assign.objects.filter(master=self, done=False, read=False).count()
		return True

	class	Meta:
		app_label = 'gw'
		verbose_name = u'Задача vEvent'
		verbose_name_plural = u'Задачи vEvent'
