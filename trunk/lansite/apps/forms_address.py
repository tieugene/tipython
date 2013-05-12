# -*- coding: utf-8 -*-
'''
lansite.apps.address.forms
'''

from django import forms

from models import *
from django.db.models import Q

        
class    SelectAddressForm(forms.Form):
    address        = forms.ModelChoiceField(queryset=Address.objects.all(), label='')
    def    setdata(self, parent_id, type_id):
        if parent_id is None:
            self.fields['address'].queryset = Address.objects.filter(id__lt=247)
        else:    
            self.fields['address'].queryset = Address.objects.filter(parent__id=parent_id, type__id=type_id)
        
class    SelectAddressTypeForm(forms.Form):
    type        = forms.ModelChoiceField(queryset=AddrShort.objects.all(), label='')
    def    setdata(self, parent_id):
        if not parent_id is None:
            self.fields['type'].queryset = AddrShort.objects.filter(id__in=Address.objects.filter(parent=parent_id).values_list('type__id'))            
        
class    ContactAddressTypeForm(forms.Form):
    type        = forms.ModelChoiceField(queryset=ContactAddrType.objects.all(), label='')
    def    setdata(self, contact_id):
        self.fields['type'].queryset = ContactAddrType.objects.filter(~Q(id__in=Contact2AddrType.objects.filter(caddr__in=ContactAddr.objects.filter(contact__id=contact_id)).values_list('type__id')))
                  
