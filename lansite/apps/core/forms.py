# -*- coding: utf-8 -*-
'''
lansite.apps.core.forms
'''

from django import forms

from models import *

class	UserListForm(forms.Form):
	user	= forms.ModelChoiceField(queryset=User.objects.all(), required=True)

class	PhoneForm(forms.ModelForm):
	#types	= forms.ModelMultipleChoiceField(queryset=PhoneType.objects.all(), widget=forms.CheckboxSelectMultiple)
	
	class	Meta:
		model = Phone
		fields = ('no',)

class	WWWForm(forms.ModelForm):
	class	Meta:
		model = WWW
		fields = ('URL',)

class	EmailForm(forms.ModelForm):
	class	Meta:
		model = Email
		fields = ('URL',)

class	IMForm(forms.ModelForm):
	class	Meta:
		model = IM
		fields = ('account', 'type',)

class	SelectCountryForm(forms.Form):
	item	= forms.ModelChoiceField(queryset=Address.objects.extra(where=['ISNULL(parent_id)']).order_by('name'), empty_label=None)
	#item.widget.attrs["onchange"]="this.form.submit()"
	#Address.objects.filter(parent__isnull=True)
	#Address.objects.filter(parent=None)
	#Address.get_root_nodes()

class	ChoiceForm(forms.Form):
	item	= forms.ModelChoiceField(queryset=None, empty_label=None)
	def	__init__(self, q, *args, **kwargs):
		super(ChoiceForm, self).__init__(*args, **kwargs)
		self.fields['item'].queryset = q

class	AddrShortForm(forms.ModelForm):
	'''
	Form to add new AddrShort
	'''
	class	Meta:
		model = AddrShort

class	AddressForm(forms.ModelForm):
	'''
	Initial + filter
	'''
	type	= forms.ModelChoiceField(queryset=None, label='Сокращение', empty_label=None)
	parent	= forms.ModelChoiceField(queryset=None, label='Предок', empty_label=None)
	def	__init__(self, addr_id, short_id, *args, **kwargs):
		super(AddressForm, self).__init__(*args, **kwargs)
		self.fields['type'].queryset = AddrShort.objects.filter(pk=int(short_id))
		self.fields['parent'].queryset = Address.objects.filter(pk=int(addr_id))

	class	Meta:
		model = Address
		fields = ('parent', 'type', 'name', 'typeplace', 'publish', 'endpoint', 'zip',)

class	AddressAddForm1(forms.ModelForm):
	type	= forms.ModelChoiceField(queryset=None, label='Сокращение', empty_label=None)
	def	__init__(self, q, *args, **kwargs):
		super(AddressAddForm1, self).__init__(*args, **kwargs)
		self.fields['type'].queryset = q

	class	Meta:
		model = Address
		fields = ('type', 'name', 'zip', 'typeplace', 'publish', 'endpoint',)

class	AddressAddForm2(forms.ModelForm):
	class	Meta:
		model = Address
		fields = ('name', 'zip', 'typeplace', 'publish', 'endpoint',)

class	AddressEditForm(forms.ModelForm):
	class	Meta:
		model = Address
		fields = ('type', 'name', 'typeplace', 'publish', 'endpoint', 'zip',)
		