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
	user = request.user
	approver = models.Approver.objects.get(pk=user.pk)
	#print approver.role.pk == 1
	queryset = models.Bill.objects.all()
	#if not request.user.is_superuser:
	#	queryset = queryset.filter(assign=request.user)
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'bills/list.html',
		extra_context = {'canadd': approver.role.pk == 1 }
	)

@login_required
def	bill_add(request):
	'''
	Add new (draft) bill
	ACL: root|Исполнитель
	So (transaction):
	- pre-save form
	- fill all fields
	- save bill
	- save m2m
	- save file
	'''
	user = request.user
	approver = models.Approver.objects.get(pk=user.pk)
	if not user.is_superuser:
		if (approver.role.pk != 1):
			return redirect('bills.views.bill_list')
	if request.method == 'POST':
		#path = request.POST['path']
		form = forms.BillAddForm(request.POST, request.FILES)
		if form.is_valid():
			# 1. bill at all
			bill = form.save(commit=False)
			image = form.cleaned_data['img']
			bill.filename	= image.name
			bill.mimetype	= image.content_type
			bill.assign	= approver
			bill.approve	= approver
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
	ACL: (root|assignee) & Draft
	'''
	user = request.user
	approver = models.Approver.objects.get(pk=user.pk)
	bill = models.Bill.objects.get(pk=int(id))
	if (not request.user.is_superuser) and (\
	   (bill.assign != approver) or\
	   (bill.get_state() != 1)):
		return redirect('bills.views.bill_view', bill.pk)
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
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {'form': form, 'object': bill}))

@login_required
def	bill_view(request, id):
	'''
	View/Accept/Reject bill
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
	ACL: (assignee & Draft & Route ok) | (approver & OnWay)
	TODO:
	+ check resume not empty on reject
	+ check resume not empty on start
	- check assign can't be in route

	'''
	user = request.user
	approver = models.Approver.objects.get(pk=user.pk)
	bill = models.Bill.objects.get(pk=int(id))
	bill_state = bill.get_state()
	form = None
	err = ''
	if (request.method == 'POST'):
		if (request.POST['resume'] in set(['accept', 'reject'])) and (\
		   ((approver == bill.assign) and (bill.get_state() == 1)) or\
		   ((approver == bill.approve) and (bill.get_state() == 2)) \
		   ):
			resume = (request.POST['resume'] == 'accept')
			form = forms.ResumeForm(request.POST)
			if form.is_valid():
				# 0. check prerequisites
				if (not resume) and (not form.cleaned_data['note']):				# resume not empty on reject
					err = 'Отказ необходимо комментировать'
				elif (bill_state == 1) and (resume) and (not form.cleaned_data['note']):	# check resume not empty on start
					err = 'Запуск по маршруту необходимо комментировать'
				elif (bill_state == 1) and (resume) and (approver in bill.route.all()):	# check resume not empty on start
					err = 'Исполнитель не должен быть в маршруте'
				else:
					# 1. new comment
					models.BillEvent.objects.create(bill=bill, user=approver, comment=form.cleaned_data['note'])
					# 2. update bill
					if resume:
						route_list = bill.route.all()
						#print route_list, len(route_list), route_list[len(route_list)-1]
						routes = bill.route.count()
						if (bill.isgood == False):			# 1st (draft)
							#print "1st"
							bill.isgood = True
							bill.approve = route_list[0]
						elif (approver == route_list[-1]):	# last
							#print "Last"
							bill.approve = bill.assign
							bill.isalive = False
						else:						# intermediate
							#print "Intermediate"
							i = 0
							found = False
							for u in route_list:
								if approver == u:
									found = True
									break
								i += 1
							if (found):
								#print 'Found:', i, 'Next:', route_list[i + 1]
								bill.approve = route_list[i + 1]
					else:
						bill.approve = bill.assign
						bill.isalive = False
						bill.isgood = False
					bill.save()
					return redirect('bills.views.bill_list')
	if (form == None):
		form = forms.ResumeForm()
	return render_to_response('bills/detail.html', context_instance=RequestContext(request, {
		'object': bill,
		'form': form,
		# root | (assignee & Draft)
		'canedit': (user.is_superuser or ((bill.assign == approver) and (bill_state == 1))),
		# root | (assignee & (Draft|Rejected)==bad)
		'candel': (user.is_superuser or ((bill.assign == approver) and (bill.isgood == False))),
		# (assignee & Draft) | (approver & OnWay)
		'canaccept': (((bill.assign == approver) and (bill_state == 1)) or ((bill.approve == approver) and (bill_state == 2))),
		# approver & OnWay
		'canreject': ((bill.approve == approver) and (bill_state == 2)),
		'err': err
	}))

@login_required
def	bill_get(request, id):
	'''
	Download bill
	ACL: any?
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
	ACL: (root|assignee) & (Draft|Rejected (bad))
	'''
	bill = models.Bill.objects.get(pk=int(id))
	if (not request.user.is_superuser) and (\
	   (bill.assign.pk != request.user.pk) or\
	   (bill.isgood == True)):
		return redirect('bills.views.bill_view', bill.pk)
	path = bill.get_path()
	if os.path.exists(path):
		os.unlink(path)
	bill.delete()
	return redirect('bills.views.bill_list')
