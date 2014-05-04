# -*- coding: utf-8 -*-
'''
TODO:
* get_object_or_404(
'''

# 1. django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context
from django.views.generic.list_detail import object_list, object_detail

# 2. system
import os, sys, pprint

# 3. 3rd party

# 4. my
import models, forms
from bills.models import Bill, Approver

PAGE_SIZE = 25

reload(sys)
sys.setdefaultencoding('utf-8')

@login_required
def	addon_list(request):
	# 1. pre
	user = request.user
	approver = Approver.objects.get(user=user)
	queryset = Bill.objects.all().order_by('-pk')
	# 3. filter by role
	#role_id = approver.role.pk
	#if (role_id == 3):	# Руководители
	#	queryset = queryset.filter(rpoint__approve=approver)
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'new/list.html',
	)

@login_required
def	addon_edit(request, id):
	approver = Approver.objects.get(pk=request.user.pk)
	# TODO: chk user <> approver
	pk = int(id)
	bill = Bill.objects.get(pk=pk)
	#addon = bill.addon.
	if (models.AddOn.objects.filter(pk=pk).count()):
		addon = models.AddOn.objects.get(pk=pk)
	else:
		addon = None
	if request.method == 'POST':
		form = forms.AddOnForm(request.POST, instance=addon)
		if form.is_valid():
			form.save()
			return redirect('new.views.addon_list')
	else:
		if (addon):
			form = forms.AddOnForm(instance = addon)
		else:
			form = forms.AddOnForm(initial={'bill':	bill})
	return render_to_response('new/form.html', context_instance=RequestContext(request, {
		'object': bill,
		'form': form,
	}))
