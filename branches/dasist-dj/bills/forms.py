# -*- coding: utf-8 -*-
'''
http://snipt.net/danfreak/how-to-generate-a-dynamic-at-runtime-form-in-django/
TODO: widget=TinyMCE(
'''

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe

import pprint

import models

#class	BillAddForm(forms.Form):
#	img = forms.ImageField()
#	project	= forms.CharField(max_length=64, verbose_name=u'Объект')
#	depart	= forms.CharField(max_length=64, verbose_name=u'Направление')

mime_available = set((
	'image/png',
	'image/tiff',
	'application/pdf',
))

class	BillForm(forms.ModelForm):
	img = forms.FileField()	# name, size, content_type, temporary_file_path,

#	def __init__ (self, *args, **kwargs):
#		super(BillForm, self).__init__(*args, **kwargs)
#		self.fields['route'].widget = forms.widgets.CheckboxSelectMultiple()
#		#self.fields["diets"].help_text = ""
#		#self.fields["diets"].queryset = Diet.objects.all()

	class Meta:
		model = models.Bill
		exclude = ('filename', 'mimetype', 'assign', 'approve', 'isalive', 'isgood', 'route')

class	BillAddForm(BillForm):
	img = forms.FileField()

	def clean_img(self):
		image = self.cleaned_data['img']
		if image.content_type not in mime_available:
			raise forms.ValidationError('File must be PNG, TIF or PDF!')
		return image

class	BillEditForm(BillForm):
	img = forms.FileField(required=False)

	def clean_img(self):
		image = self.cleaned_data['img']
		if image:
			if image.content_type not in mime_available:
				raise forms.ValidationError('File must be PNG, TIF or PDF!')
		return image

class	BillRouteForm(forms.Form):
	approve = forms.ModelChoiceField(queryset=models.Approver.objects.all())

BillRouteFormSetFactory = formset_factory(BillRouteForm, extra=1)
