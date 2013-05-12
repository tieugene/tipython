# -*- coding: utf-8 -*-
'''
lansite.apps.tagged.forms
'''

from django import forms

from models import *
from apps.file.models import File
from django.contrib.contenttypes.models import ContentType
#from apps.tagged.views import get_not_tagged


def get_not_tagged(model):
    list=model.objects.all()
    tos=TaggedObject.objects.all()
    ids=[]
    for to in tos:
        ids.append(to.object.id)
    list=list.exclude(id__in=ids)
    ids2=[]
    for item in list:
        ids2.append(item.id)
    list.ids=ids2
    return list

class    TaggedObjectForm(forms.ModelForm):
    object        = forms.ModelChoiceField(queryset=get_not_tagged(File), required=True)
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = TaggedObject
        fields = ('object','tot')

class    TagTypeForm(forms.ModelForm):
    type = forms.ChoiceField(choices=[(0, "Строка"),(1, "Триггер"),(2, "Число"),(3, "Дата"),(4, "Объект")], label='Тип тэга')
    multiplicity = forms.ChoiceField(choices=[(0, "Единств. - Не обязательн."),(1, "Единств. - Обязательн."),(2, "Множеств. - Обязательн."),(3, "Множеств. - Не обязательн.")], label='Множественность', initial=3)
    error_css_class = 'error'
    required_css_class = 'required'
    type.widget.attrs["onchange"]="objSel()"
    class    Meta:
        model = TaggedObjectTagType

class    ObjTypeForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class    Meta:
        model = TaggedObjectType

class TypeListForm(forms.Form):
    type    = forms.ModelChoiceField(queryset=TaggedObjectType.objects.all(), label='Тип')

class ContentTypeListForm(forms.Form):
    type    = forms.ModelChoiceField(queryset=ContentType.objects.all(), label='Тип')

class ObjectListForm(forms.Form):
    object = forms.ModelChoiceField(queryset='', label='Объект')

class TagTypeListForm(forms.Form):
    type    = forms.ModelChoiceField(queryset=TaggedObjectTagType.objects.all(), label='Тип')
