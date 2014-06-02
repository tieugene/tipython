# -*- coding: utf-8 -*-

from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from models import Scan

EMPTY_VALUE = [('', '---'),]

class	FilterScanListForm(forms.Form):
	#place		= forms.ChoiceField(choices=Scan.objects.order_by('place').distinct().values_list('place', 'place'), label=u'Объект', required=False)
	place		= forms.ChoiceField(choices=EMPTY_VALUE + list(Scan.objects.order_by('place').distinct().values_list('place', 'place')), label=u'Объект', required=False)
#	#subject
	depart		= forms.ChoiceField(choices=EMPTY_VALUE + list(Scan.objects.order_by('depart').distinct().values_list('depart', 'depart')), label=u'Направление', required=False)
	supplier	= forms.CharField(max_length=64, label=u'Поставщик', required=False)
	billno		= forms.CharField(max_length=64, label=u'Номер счета', required=False)
	billdate	= forms.DateField(label=u'Дата счета', required=False)