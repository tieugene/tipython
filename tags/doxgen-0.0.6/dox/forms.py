# -*- coding: utf-8 -*-
'''
http://snipt.net/danfreak/how-to-generate-a-dynamic-at-runtime-form-in-django/
'''

from django import forms
from django.forms.formsets import formset_factory
from django.utils.datastructures import SortedDict

from consts import *

field_dict = {
	K_BOOL_FIELD:	forms.BooleanField,
	K_CHAR_FIELD:	forms.CharField,
	K_DATE_FIELD:	forms.DateField,
	K_DEC_FIELD:	forms.DecimalField,
	K_CHOICE_FIELD:	forms.ChoiceField,
}

def	GenForm(fieldlist, named=True):	# FIXME: form name (for formset class name)
	'''
	Generates Form class
	:param fieldlist:SortedDict - fields definitions
	Return form class
	'''
	fields = SortedDict()
	if (named):
		fields[K_T_F_NAME] = forms.CharField(label='Наименование', help_text='уникальное для данного типа документов')
	for k, v in fieldlist.iteritems():
		fields[k] = field_dict[v[K_T_FIELD_T]](**v[K_T_FIELD_A])
	return type('DynaForm', (forms.BaseForm,), { 'base_fields': fields })

# formset = formset_factory(OkvedForm)(request.POST)
# or
# MyFormSet = formset_factory(OkvedForm); formset = MyFormSet()
# So - class formset_factory(class)

def	GenFormSets(formlist):
	'''
	Generates SortedDict of Form sets classes
	:param fieldlist:SortedDict - fields sets definitions
	:return SortedDict { k: formset class }
	'''
	retvalue = SortedDict()
	for k, v in formlist.iteritems():	# i:str - formset key, j:{ K_T_FIELD_A: {}, K_T_FIELD_T: SortedDict() } - of fields definitions
		retvalue[k] = formset_factory(GenForm(v[K_T_FIELD_T], named = False))
	return retvalue
