# -*- coding: utf-8 -*-
'''
lansite.gw.forms.py
'''
from address.forms import *
from bits.forms import *
from contact.forms import *
from file.forms import *
from tagged.forms import *
from task.forms import *
from django.contrib.auth.models import Group

class    WordCombinationEditForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = WordCombination


class    PermissionAddForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='')
    def    setdata(self, contenttype_id):
        self.fields['group'].queryset = Group.objects.filter(
                ~Q(id__in=Permissions.objects.filter(model=contenttype_id, subject=False).values('subject')))


