# -*- coding: utf-8 -*-
'''
TODO:
* get_object_or_404(
'''

# 1. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.utils.datastructures import SortedDict

# 2. system
import os, imp, pprint, tempfile

# 3. 3rd party

# 4. my
import models, forms

PAGE_SIZE = 20

@login_required
def	bill_list(request):
	'''
	List of bills
	ACL: assign|approve=user
	'''
	#if request.user.is_authenticated():
	#	queryset = models.Doc.objects.filter(user=request.user, type=uuid).order_by('name')
	#else:
	#	queryset = models.Doc.objects.none()
	queryset = models.Bill.objects.all()
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'bills/list.html',
	)

@login_required
def	bill_add(request):
	'''
	Add new (draft) bill
	So (transaction):
	- pre-save form
	- fill all fields
	- save bill
	- save m2m
	- save file
	'''
	if request.method == 'POST':
		#path = request.POST['path']
		form = forms.BillAddForm(request.POST, request.FILES)
		if form.is_valid():
			# 1. bill at all
			bill = form.save(commit=False)
			image = form.cleaned_data['img']
			bill.filename	= image.name
			bill.mimetype	= image.content_type
			bill.assign	= request.user
			bill.approve	= request.user
			bill.isalive	= True
			bill.isgood	= False
			bill.save()
			# 2. route
			form.save_m2m()
			# 3. file
			with open(bill.get_path(), 'wb') as file:
				file.write(image.read())
			# x. the end
			return redirect('bills.views.bill_view', bill.pk)
			try:
				os.makedirs(file.get_full_dir())
				os.rename(src_path, file.get_full_path())
			except:
				transaction.rollback()
			else:
				return redirect('bills.views.bill_list')
	else:
		form = forms.BillAddForm()
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {'form': form,}))

@login_required
def	bill_edit(request, id):
	'''
	Update (edit) bill
	'''
	bill = models.Bill.objects.get(pk=int(id))
	if request.method == 'POST':
		form = forms.BillEditForm(request.POST, request.FILES, instance = bill)
		if form.is_valid():
			bill = form.save(commit=False)
			image = form.cleaned_data['img']
			if image:
				bill.filename	= image.name
				bill.mimetype	= image.content_type
				with open(bill.get_path(), 'wb') as file:
					file.write(image.read())
			bill.save()
			form.save_m2m()
			return redirect('bills.views.bill_view', bill.pk)
	else:
		form = forms.BillEditForm(instance = bill)
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {'form': form,}))

@login_required
def	bill_view(request, id):
	'''
	Read (view) bill
	'''
	return  object_detail (
		request,
		queryset = models.Bill.objects.all(),
		object_id = id,
		template_name = 'bills/detail.html',
	)

@login_required
def	bill_get(request, id):
	'''
	Download bill
	'''
	bill = models.Bill.objects.get(pk=int(id))
	response = HttpResponse(mimetype=bill.mimetype)
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = '; filename=' + bill.filename
	response.write(open(bill.get_path()).read())
	return response


@login_required
def	bill_delete(request, id):
	'''
	Delete bill
	'''
	bill = models.Bill.objects.get(pk=int(id))
	path = bill.get_path()
	if os.path.exists(path):
		os.unlink(path)
	bill.delete()
	return redirect('bills.views.bill_list')

@login_required
def	bill_accept(request, id):
	'''
	Accept bill
	'''
	return __doc_rvp(request, id, 1)

@login_required
def	bill_reject(request, id):
	'''
	Reject bill
	'''
	return __doc_rvp(request, id, 2)

