# -*- coding: utf-8 -*-
'''
lansite.gw.task.forms.py
'''

from django import forms

from models import *

class	ToDoCatForm(forms.ModelForm):
	class	Meta:
		model = ToDoCat
		fields = ('name',)

class	ToDoForm(forms.ModelForm):
	class	Meta:
		model = ToDo
		#exclude = ('ancestor', 'master', 'author', 'created')
		fields = ('deadline', 'subject', 'description', 'done', 'category')

class	ToDoOfCatForm(forms.ModelForm):
	class	Meta:
		model = ToDo
		fields = ('deadline', 'subject', 'description', 'done',)

class	ToDoCatFilterForm(forms.Form):
	f_cat	= forms.ModelChoiceField(queryset=ToDoCat.objects.all())
	f_state	= forms.ChoiceField(choices=((0, '---'), (1, 'Opened'), (2, 'Done')))
	s_0	= forms.ChoiceField()
	s_1	= forms.ChoiceField()
	s_2	= forms.ChoiceField()
	s_3	= forms.ChoiceField()
	s_4	= forms.ChoiceField()

	def	__init__(self, q, *args, **kwargs):
		super(ToDoCatFilterForm, self).__init__(*args, **kwargs)
		self.fields['f_cat'].queryset = q
		for i in xrange(5):
			self.fields['s_%d' % i].choices = ((0, '-'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))

class	AssignCatForm(forms.ModelForm):
	class	Meta:
		model = AssignCat

class	AssignForm(forms.ModelForm):
	class	Meta:
		model = Assign
		fields = ('deadline', 'subject', 'description', 'category', 'importance', 'assignee')

class	LineCommentForm(forms.Form):
	comment	= forms.CharField(label='Причина')

class	AssignDupForm(forms.Form):
	assign	= forms.ModelChoiceField(queryset=Assign.objects.all(), required=True)
