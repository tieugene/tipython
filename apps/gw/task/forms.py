# -*- coding: utf-8 -*-
'''
lansite.gw.task.forms.py
'''

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.core.validators import ValidationError

from models import *

SORT_CHOICES = ((0, '---'), (1, "Down"), (2, "Up"),)

class	CategoryForm(forms.ModelForm):
	thisuser	= forms.BooleanField(label='Только для меня', required=False)
	thisapp		= forms.BooleanField(label='Только для Задач', required=False)

	class	Meta:
		model = Category
		exclude = ('user', 'app',)

class	ToDoForm(forms.ModelForm):
	'''
	Try widgets:
	* SplitDateTimeWidget
	* SelectDateWidget
	FIXME: not all Categories
	'''
	# status		= forms.TypedChoiceField(choices=VTODO_STATUS_CHOICES, label='Состояние', required=False, empty_value=None)
	start_d		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateInput(format="%m.%d.%Y"), label='Начало (дата)', required=False)
	due_d		= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateInput(format="%m.%d.%Y"), label='До (дата)', required=False)
	percent		= forms.IntegerField(min_value=0, max_value=100, label='Процент', required=False)
	categories	= forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=CheckboxSelectMultiple())

	class	Meta:
		model = vToDo
		exclude = ('user', 'created', 'updated', 'links')


	# Overriding save allows us to process the value of 'categories' field    
	def	save(self, commit=True):
		instance = forms.ModelForm.save(self, False)	# Get the unsave ToDo instance
		def	save_m2m():
			# This is where we actually link the pizza with toppings
			instance.taskcat_set.all().delete()
			for cat in self.cleaned_data['categories']:
				instance.taskcat_set.create(task=instance, cat=cat)
		self.save_m2m = save_m2m
		if commit:					# Do we need to save all changes now?
			instance.save()
			self.save_m2m()
		return instance

class	ChoiceForm(forms.Form):
	'''
	From gw.bits
	'''
	item	= forms.ModelChoiceField(queryset=None, empty_label=None)
	def	__init__(self, q, *args, **kwargs):
		super(ChoiceForm, self).__init__(*args, **kwargs)
		self.fields['item'].queryset = q

class	FileUploadForm(forms.Form):
	file	= forms.FileField(label='Файл *.ics')

class	ColumnsForm(forms.Form):
	'''
	Select columns to show
	'''
	user		= forms.BooleanField(label="Автор", required=False, initial=True)
	created		= forms.BooleanField(label="Создано", required=False, initial=True)
	updated		= forms.BooleanField(label="Изменено", required=False, initial=True)
	summary		= forms.BooleanField(label="Тема", required=False, initial=True)
	status		= forms.BooleanField(label="Состояние", required=False, initial=True)
	restriction	= forms.BooleanField(label="Видимость", required=False, initial=True)
	categories	= forms.BooleanField(label="Категории", required=False, initial=True)
	attendee	= forms.BooleanField(label="Участник", required=False, initial=True)
	start		= forms.BooleanField(label="Начало", required=False, initial=True)
	duration	= forms.BooleanField(label="Длительность", required=False, initial=True)
	priority	= forms.BooleanField(label="Приоритет", required=False, initial=True)
	due		= forms.BooleanField(label="До", required=False, initial=True)
	completed	= forms.BooleanField(label="Завершено", required=False, initial=True)
	percent		= forms.BooleanField(label="%", required=False, initial=True)
	"""
	def setData(self, kwds):
		'''
		Set the data to include in the form
		@param kwds:dict { <fldname>: <fldvalue> }
		'''
		keys = kwds.keys()
		for k in keys:
			self.fields[k].initial = kwds[k]
	"""
	def getData(self):
		retvalue = dict()
		for f in self.fields.items():
			retvalue[f[0]] = self.cleaned_data[f[0]]
		return retvalue

class	SortForm(forms.Form):
	'''
	Set sorting
	'''
	user		= forms.TypedChoiceField(label="Автор", required=False, choices=SORT_CHOICES)
	created		= forms.TypedChoiceField(label="Создано", required=False, choices=SORT_CHOICES)
	updated		= forms.TypedChoiceField(label="Изменено", required=False, choices=SORT_CHOICES)
	summary		= forms.TypedChoiceField(label="Тема", required=False, choices=SORT_CHOICES)
	status		= forms.TypedChoiceField(label="Состояние", required=False, choices=SORT_CHOICES)
	restriction	= forms.TypedChoiceField(label="Видимость", required=False, choices=SORT_CHOICES)
	attendee	= forms.TypedChoiceField(label="Участник", required=False, choices=SORT_CHOICES)
	start		= forms.TypedChoiceField(label="Начало", required=False, choices=SORT_CHOICES)
	duration	= forms.TypedChoiceField(label="Длительность", required=False, choices=SORT_CHOICES)
	priority	= forms.TypedChoiceField(label="Приоритет", required=False, choices=SORT_CHOICES)
	due		= forms.TypedChoiceField(label="До", required=False, choices=SORT_CHOICES)
	completed	= forms.TypedChoiceField(label="Завершено", required=False, choices=SORT_CHOICES)
	percent		= forms.TypedChoiceField(label="%", required=False, choices=SORT_CHOICES)

	def getData(self):
		retvalue = dict()
		for f in self.fields.items():
			retvalue[f[0]] = int(self.cleaned_data[f[0]])
		return retvalue

class	FilterForm(forms.Form):
	'''
	Set filter
	'''
	user		= forms.ModelChoiceField(queryset=GwUser.objects.all(), required=False, label="Автор")
	#user		= forms.TypedChoiceField(label="Автор", required=False, choices=[(0, '---'),])
	status		= forms.TypedChoiceField(label="Состояние", required=False, choices=[(0, '---'),]+list(VTODO_STATUS_CHOICES))
	restriction	= forms.TypedChoiceField(label="Видимость", required=False, choices=[(0, '---'),]+list(RESTRICTION_CHOICES))
	#attendee	= forms.TypedChoiceField(label="Участник", required=False, choices=[(0, '---'),])
	attendee	= forms.ModelChoiceField(queryset=GwUser.objects.all(), required=False, label="Участник")
	priority	= forms.TypedChoiceField(label="Приоритет", required=False, choices=[(0, '---'),]+list(PRIORITY_CHOICES))

	def getData(self):
		retvalue = dict()
		for f in self.fields.items():
			name = f[0]
			v = self.cleaned_data[f[0]]
			if name in ('user', 'attendee'):
				if v:
					v = v.pk
				else:
					v = 0
			else:
				v = int(v)
			retvalue[name] = v
		return retvalue
