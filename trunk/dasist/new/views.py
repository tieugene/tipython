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
def	addon_add(request):
	'''
	'''
	user = request.user
	#approver = models.Approver.objects.get(pk=user.pk)	# !!!
	approver = models.Approver.objects.get(user=user)	# !!!
	#if not user.is_superuser:
	#	if (approver.role.pk != 1):
	#		return redirect('bills.views.bill_list')
	if request.method == 'POST':
		#path = request.POST['path']
		form = forms.BillAddForm(request.POST, request.FILES)
		if form.is_valid():
			# 1. create fileseq
			fileseq = FileSeq()
			fileseq.save()
			# 2. convert image and add to fileseq
			__update_fileseq(request.FILES['file'], fileseq, form.cleaned_data['rawpdf'])
			# 3. bill at all
			bill = models.Bill(
				fileseq		= fileseq,
				place		= form.cleaned_data['place'],
				subject		= form.cleaned_data['subject'],
				depart		= form.cleaned_data['depart'],
				payer		= form.cleaned_data['payer'],
				supplier	= form.cleaned_data['supplier'],
				billno		= form.cleaned_data['billno'],
				billdate	= form.cleaned_data['billdate'],
				billsum		= form.cleaned_data['billsum'],
				payedsum	= form.cleaned_data['payedsum'],
				topaysum	= form.cleaned_data['topaysum'],
				assign		= approver,
				rpoint		= None,
				done		= None,
			)
			bill.save()
			# 4. add route
			std_route1 = [	# role_id, approve_id
				(2, models.Approver.objects.get(pk=13)),	# начОМТС
				(3, form.cleaned_data['approver']),		# Руководитель
				(4, None),					# Директор
				(5, models.Approver.objects.get(pk=3)),		# Гендир
				#(6, models.Approver.objects.get(pk=4)),	# Бухгалтер
				(6, None),					# Бухгалтер
			]
			for i, r in enumerate(std_route1):
				bill.route_set.add(
					models.Route(
						bill	= bill,
						order	= i+1,
						role	= models.Role.objects.get(pk=r[0]),
						approve	= r[1],
					),
				)
			#bill = form.save(commit=False)
			return redirect('bills.views.bill_view', bill.pk)
	else:
		form = forms.BillAddForm()
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {
		'form': form,
		'places': models.Place.objects.all(),
	}))

@login_required
def	addon_edit(request, id):
	'''
	Update (edit) bill
	ACL: (assignee) & Draft
	'''
	user = request.user
	approver = models.Approver.objects.get(pk=user.pk)
	bill = models.Bill.objects.get(pk=int(id))
	#if (not request.user.is_superuser) and (\
	#   (bill.assign != approver) or\
	#   (bill.rpoint != None) or\
	#   (bill.done != None)):
	#	return redirect('bills.views.bill_view', bill.pk)
	if request.method == 'POST':
		form = forms.BillEditForm(request.POST, request.FILES)
		if form.is_valid():
			tosave = False
			# 1. update bill
			def	chk_fld(form, fld, fldname):
				if (fld != form.cleaned_data[fldname]):
					fld = form.cleaned_data[fldname]
					return True
				else:
					return False
			bill.place= form.cleaned_data['place']
			bill.subject= form.cleaned_data['subject']
			bill.depart= form.cleaned_data['depart']
			bill.payer= form.cleaned_data['payer']
			bill.supplier= form.cleaned_data['supplier']
			bill.billno= form.cleaned_data['billno']
			bill.billdate= form.cleaned_data['billdate']
			bill.billsum= form.cleaned_data['billsum']
			bill.payedsum= form.cleaned_data['payedsum']
			bill.topaysum= form.cleaned_data['topaysum']
			#if (tosave):
			bill.save()
			# 2. update approver (if required)
			special = bill.route_set.get(order=2)	# Аня
			if (special.approve != form.cleaned_data['approver']):
				special.approve = form.cleaned_data['approver']
				special.save()
			# 3. update image
			file = request.FILES.get('file', None)
			if (file):
				fileseq = bill.fileseq
				fileseq.clean_children()
				__update_fileseq(file, fileseq, form.cleaned_data['rawpdf'])	# unicode error
			return redirect('bills.views.bill_view', bill.pk)
	else:
		form = forms.BillEditForm(initial={
			'place':	bill.place,
			'subject':	bill.subject,
			'depart':	bill.depart,
			'payer':	bill.payer,
			'supplier':	bill.supplier,
			'billno':	bill.billno,
			'billdate':	bill.billdate,
			'billsum':	bill.billsum,
			'payedsum':	bill.payedsum,
			'topaysum':	bill.topaysum,
			'approver':	bill.route_set.get(order=2).approve,	# костыль
			#'approver':	6,
		})
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': bill,
		'places': models.Place.objects.all(),
	}))

@login_required
def	addon_view(request, id):
	'''
	View/Accept/Reject bill
	ACL: (assignee & Draft & Route ok) | (approver & OnWay)
	'''
	user = request.user
	approver = models.Approver.objects.get(user=user)
	bill = models.Bill.objects.get(pk=int(id))
	bill_state_id = bill.get_state_id()
	form = None
	err = ''
	if (request.method == 'POST'):
		if (request.POST['resume'] in set(['accept', 'reject'])) and (\
		   ((bill_state_id == 1) and (approver == bill.assign)) or\
		   (((bill_state_id == 2) or (bill_state_id == 3)) and ( \
			((bill.rpoint.approve != None) and (approver == bill.rpoint.approve)) or\
			((bill.rpoint.approve == None) and (approver.role == bill.rpoint.role))\
		    ) \
		    )
		   ):
			resume = (request.POST['resume'] == 'accept')
			form = forms.ResumeForm(request.POST)
			if form.is_valid():
				# 0. check prerequisites
				if (not resume) and (not form.cleaned_data['note']):				# resume not empty on reject
					err = 'Отказ необходимо комментировать'
				#elif (bill_state_id == 1) and (not form.cleaned_data['note']):	# check resume not empty on start
				#	err = 'Запуск по маршруту необходимо комментировать'
				else:
					# 1. new comment
					models.Event.objects.create(
						bill=bill,
						approve=approver,
						resume=resume,
						comment=form.cleaned_data['note']
					)
					# 2. update bill
					if resume:
						route_list = bill.route_set.all().order_by('order')
						if (bill_state_id == 1):				# 1. 1st (draft)
							bill.rpoint = route_list[0]
						else:
							rpoint = bill.rpoint
							if (rpoint.order == len(route_list)):		# 2. last
								if (bill.done == None):		# to pay
									bill.done = True
								else:				# done
									bill.rpoint = None
							else:						# 3. intermediate
								bill.rpoint = bill.route_set.get(order=rpoint.order+1)
					else:	# Reject
						bill.rpoint = None
						bill.done = False
					bill.save()
					if (bill.done == True) and (bill.rpoint == None):
						bill.rpoint = bill.route_set.all().delete()
					__mailto(request, bill)
					return redirect('bills.views.bill_list')
	if (form == None):
		form = forms.ResumeForm()
	return render_to_response('bills/detail.html', context_instance=RequestContext(request, {
		'object': bill,
		'form': form,
		'canedit':	## assignee & Draft
			(user.is_superuser or ((bill_state_id == 1) and (bill.assign == approver))),
		'candel':	## assignee & (Draft|Rejected)==bad)
			(user.is_superuser or (((bill_state_id == 1) or (bill_state_id == 5)) and (bill.assign == approver))),
		'canaccept':	## (assignee & Draft) | (approver & OnWay)
			(
			((bill_state_id == 1) and (bill.assign == approver)) or\
			(((bill_state_id == 2) or (bill_state_id == 3)) and (
			  ((bill.rpoint.approve != None) and (bill.rpoint.approve == approver)) or\
			  ((bill.rpoint.approve == None) and (bill.rpoint.role == approver.role))\
			 )\
			)\
		),
		'canreject':	## not Accounter
			approver.role.pk != 6,
		'canarch':	## assignee & Done
			(user.is_superuser or ((bill_state_id == 4) and (bill.assign == approver))),
		'canrestart':	## assignee & Rejected
			(user.is_superuser or ((bill_state_id == 5) and (bill.assign == approver))),
		'err': err
	}))
