# -*- coding: utf-8 -*-
'''
lansite.apps.task.forms.py
'''

from django import forms

from models import *

class	FileAddForm(forms.ModelForm):
	class	Meta:
		model = File
		fields = ('file',)

class	FileEditForm(forms.ModelForm):
	class	Meta:
		model = File
		fields = ('name',)

