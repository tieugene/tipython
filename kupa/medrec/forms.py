# -*- coding: utf-8 -*-

from django import forms
from django.forms.extras import SelectDateWidget

import datetime

import models, views

DURAT = [
	(0, '0:30'),
	(1, '1:00'),
	(2, '1:30'),
	(3, '2:00'),
	(4, '2:30'),
	(5, '3:00'),
	(6, '3:30'),
	(7, '4:00'),
]

class	FilterForm(forms.Form):
	date	= forms.DateField(label=u'Дата', required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
	#date	= forms.DateField(label=u'Дата', required=True, widget=SelectDateWidget(years=xrange(2010, 2020)))

class	FileForm(forms.Form):
	file	= forms.ImageField(label=u'Дата', required=False)

Client2Clean = ('lname', 'fname', 'mname', 'price', 'phone1', 'phone2', 'comment', 'details')

class	ClientForm(forms.ModelForm):
	#new	= forms.BooleanField(widget=forms.CheckboxInput(attrs={'readonly':'readonly'}))

	class Meta:
		model = models.Client
		exclude = ['user', 'name', 'birthday', 'new', 'invidate', 'invidesc']

	def clean(self):
		cleaned_data = super(ClientForm, self).clean()
		for i in Client2Clean:
			cleaned_data[i] = cleaned_data.get(i, '').strip()
		return cleaned_data

class	RecordForm(forms.ModelForm):
	time	= forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
	durat	= forms.ChoiceField(choices = DURAT)

	class Meta:
		model = models.Record
		exclude = ['user', 'client', 'code', 'state']

	def	clean(self):
		cleaned_data = super(RecordForm, self).clean()
		cleaned_data['comment'] = cleaned_data.get('comment', '').strip()
		cleaned_data['medrec'] = cleaned_data.get('medrec', '').strip()
		if ('date' in cleaned_data) and ('time' in cleaned_data):
			time = cleaned_data['time']
			if (time.hour < 8) or (time.hour > 22):
				self.add_error('time', "Time must be in 08:00..22:30")
			if (time.minute not in set((0, 30))):
				self.add_error('time', "Minute must be 00 or 30")
		return cleaned_data
