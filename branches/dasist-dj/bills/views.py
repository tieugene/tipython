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
	ACL: user=assign|approve|root
	'''
	queryset = models.Bill.objects.all()
	#if not request.user.is_superuser:
	#	queryset = queryset.filter(assign=request.user)
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
		extra_context = {
			'form': forms.ResumeForm(),
		},
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
def	bill_resume(request, id):
	'''
	Accept/Reject bill
	* create note
	* update bill:
	-- if accept:
	+-- case 1st (history len = 0 (bad) | approve == assign | user == approve | Draft):
	+--- approve = next (2nd) in route
	+--- isgood = True
	--- case last (user = route.last()):
	---- approve = assignee
	---- isalive = False
	--- case intermediate:
	---- approve = next in route
	+- if reject:
	+--- approve = assignee
	+--- isalive = False
	+--- isgood = False
	* goto list
	'''
	if request.POST['resume'] in set(['accept', 'reject']):
		resume = (request.POST['resume'] == 'accept')
		bill = models.Bill.objects.get(pk=int(id))
		user = request.user
		form = forms.ResumeForm(request.POST)
		if form.is_valid():
			#return redirect('bills.views.bill_list')
			# 1. new comment
			models.BillEvent.objects.create(bill=bill, user=user, comment=form.cleaned_data['note'])
			# 2. update bill
			if resume:
				user_list = bill.route.all()
				#print user_list, len(user_list), user_list[len(user_list)-1]
				routes = bill.route.count()
				if (bill.isgood == False):			# 1st (draft)
					#print "1st"
					bill.isgood = True
					bill.approve = user_list[0]
				elif (user == user_list[len(user_list)-1]):	# last
					#print "Last"
					bill.approve = bill.assign
					bill.isalive = False
				else:						# intermediate
					#print "Intermediate"
					i = 0
					found = False
					for u in user_list:
						if user == u:
							found = True
							break
						i += 1
					if (found):
						print 'Found:', i, 'Next:', user_list[i + 1]
						bill.approve = user_list[i + 1]
			else:
				bill.approve = bill.assign
				bill.isalive = False
				bill.isgood = False
			bill.save()
	return redirect('bills.views.bill_list')
