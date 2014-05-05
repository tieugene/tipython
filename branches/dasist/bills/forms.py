# -*- coding: utf-8 -*-
'''
'''

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.db.models.fields.files import FieldFile

#import models
from bills.models import Approver, Place, Subject, Department, Payer
from scan.models import Scan

#class	BillAddForm(forms.Form):
#	img = forms.ImageField()
#	project	= forms.CharField(max_length=64, verbose_name=u'Объект')
#	depart	= forms.CharField(max_length=64, verbose_name=u'Направление')

mime_available = set((
	'image/png',
	'image/tiff',
	'image/jpeg',
	'application/pdf',
))

class ApproverModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_fio()

class	BillAddForm(forms.Form):
	file		= forms.FileField(label=u'Скан')
	rawpdf		= forms.BooleanField(label=u'Конвертировать PDF', required=False)
	place		= forms.ModelChoiceField(queryset=Place.objects.all(), empty_label=None, label=u'Объект')
	subject		= forms.ModelChoiceField(queryset=Subject.objects.all(), label=u'Подобъект', required=False)
	depart		= forms.ModelChoiceField(queryset=Department.objects.all(), label=u'Направление', required=False)
	payer		= forms.ModelChoiceField(queryset=Payer.objects.all(), empty_label=None, label=u'Плательщик')
	supplier	= forms.CharField(max_length=64, label=u'Поставщик')
	billno		= forms.CharField(max_length=64, label=u'Номер счета')
	billdate	= forms.DateField(label=u'Дата счета')
	billsum		= forms.IntegerField(min_value=0, label=u'Сумма счета')
	payedsum	= forms.IntegerField(min_value=0, label=u'Оплачено')
	topaysum	= forms.IntegerField(min_value=0, label=u'Сумма к оплате')
	approver	= ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=3), empty_label=None, label=u'Руководитель', widget=forms.RadioSelect)

	def clean_file(self):
		file = self.cleaned_data['file']
		if (not isinstance(file, FieldFile)) and (file.content_type not in mime_available):
			raise forms.ValidationError('File must be PNG, TIF, JPG or PDF!')
		return None

class	BillEditForm(forms.Form):
	file		= forms.FileField(label=u'Скан', required=False, help_text=u'(Выберите файл, если хотите заменить скан)')
	rawpdf		= forms.BooleanField(label=u'Конвертировать PDF', required=False)
	place		= forms.ModelChoiceField(queryset=Place.objects.all(), empty_label=None, label=u'Объект')
	subject		= forms.ModelChoiceField(queryset=Subject.objects.all(), label=u'Подобъект', required=False)
	depart		= forms.ModelChoiceField(queryset=Department.objects.all(), label=u'Направление', required=False)
	payer		= forms.ModelChoiceField(queryset=Payer.objects.all(), empty_label=None, label=u'Плательщик')
	supplier	= forms.CharField(max_length=64, label=u'Поставщик')
	billno		= forms.CharField(max_length=64, label=u'Номер счета')
	billdate	= forms.DateField(label=u'Дата счета')
	billsum		= forms.IntegerField(min_value=0, label=u'Сумма счета')
	payedsum	= forms.IntegerField(min_value=0, label=u'Оплачено')
	topaysum	= forms.IntegerField(min_value=0, label=u'Сумма к оплате')
	approver	= ApproverModelChoiceField(queryset=Approver.objects.filter(role__pk=3), empty_label=None, label=u'Руководитель', widget=forms.RadioSelect)

	def clean_file(self):
		file = self.cleaned_data['file']
		if (file):
			if (not isinstance(file, FieldFile)) and (file.content_type not in mime_available):
				raise forms.ValidationError('File must be PNG, TIF, JPG or PDF!')
		return None

class	ResumeForm(forms.Form):
	note	= forms.CharField(label='Комментарий', required = False)

class	FilterStateForm(forms.Form):
	draft	= forms.BooleanField(label='Черновики',	required = False)
	onway	= forms.BooleanField(label='В пути',	required = False)
	onpay	= forms.BooleanField(label='В оплате',	required = False)
	done	= forms.BooleanField(label='Исполнены',	required = False)
	dead	= forms.BooleanField(label='Завернуты',	required = False)

#class	ScanAddForm(forms.ModelForm):
#	fileseq = forms.IntegerField(widget=forms.HiddenInput())
#	class	Meta:
#		model = Scan