# -*- coding: utf-8 -*-
'''
lansite.gw.contact.forms.py
'''

from django import forms

from models import *

class	ContactAddressForm(forms.ModelForm):
    types	= forms.ModelMultipleChoiceField(queryset=ContactAddrType.objects, widget=forms.CheckboxSelectMultiple, required=False)
    class	Meta:
        model = ContactAddr
        fields = ('types',)

class	ContactPhoneForm(forms.Form):
    no	= forms.CharField(label='Номер', required=True)
    ext	= forms.CharField(label='Добавочный', required=False)

class	ContactWWWForm(forms.Form):
    URL	= forms.URLField(label='URL', required=True)

class	ContactEmailForm(forms.Form):
    URL	= forms.EmailField(label='URL', required=True)

class	PersonForm(forms.ModelForm):
    birthdate	= forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата рождения', required=False)

    class	Meta:
        model = Person
        fields = ('lastname', 'firstname', 'midname', 'birthdate', 'sex')

class PersonStuffForm(forms.ModelForm):
    org	= forms.ModelChoiceField(queryset=Org.objects.all(), empty_label=None)
    role	= forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)

    class	Meta:
        model = OrgStuff
        fields = ('org', 'role',)

class	OrgForm(forms.ModelForm):
    class	Meta:
        model = Org
        fields = ('name', 'shortname', 'fullname', 'brandname', 'egruldate', 'inn', 'kpp', 'ogrn',)

class	OrgStuffForm(forms.ModelForm):
    person	= forms.ModelChoiceField(queryset=Person.objects.all(), empty_label=None)
    role	= forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)

    class	Meta:
        model = OrgStuff
        fields = ('person', 'role',)

class	RoleForm(forms.ModelForm):
    class	Meta:
        model = Role