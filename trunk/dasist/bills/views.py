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
from django.db.models import F
from django.core.files.storage import default_storage	# MEDIA_ROOT
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

# 2. system
import os, imp, pprint, tempfile, subprocess

# 3. 3rd party
from pyPdf import PdfFileReader
from pdfrw import PdfReader
from PIL import Image as PIL_Image
from wand.image import Image as Wand_Image

# 4. my
import models, forms
from core.models import File, FileSeq

PAGE_SIZE = 20
FSNAME = 'fstate'	# 0..3

def	__set_filter_state(q, s):
	'''
	q - original QuerySet (all)
	s - state (0..15)
	'''
	if   (s ==  0): return q.none()
	elif   (s ==  1): return q.filter(isalive = False, isgood = False)
	elif   (s ==  2): return q.filter(isalive = False, isgood = True)
	elif   (s ==  3): return q.filter(isalive = False)
	elif   (s ==  4): return q.filter(isalive = True, isgood = False)
	elif   (s ==  5): return q.filter(isgood = False)
	elif   (s ==  6): return q.exclude(isalive = F('isgood'))
	elif   (s ==  7): return q.exclude(isalive = True, isgood = True)
	elif   (s ==  8): return q.filter(isalive = True, isgood = True)
	elif   (s ==  9): return q.filter(isalive = F('isgood'))
	elif   (s == 10): return q.filter(isgood = True)
	elif   (s == 11): return q.exclude(isalive = True, isgood = False)
	elif   (s == 12): return q.filter(isalive = True)
	elif   (s == 13): return q.exclude(isalive = False, isgood = True)
	elif   (s == 14): return q.exclude(isalive = False, isgood = False)
	else: return q

@login_required
def	bill_list(request):
	'''
	List of bills
	ACL: user=assign|approve|root
	'''
	# 1. pre
	user = request.user
	approver = models.Approver.objects.get(user=user)
	#print approver.role.pk == 1
	queryset = models.Bill.objects.all()
	# 2. filter
	fsfilter = request.session.get(FSNAME, None)# int 0..15: dropped|done|onway|draft
	if (fsfilter == None):
		fsfilter = 15
		request.session[FSNAME] = fsfilter
	else:
		fsfilter = int(fsfilter)
	#print 'List:', fsfilter
	fsform = forms.FilterStateForm(initial={
		'dead'	:bool(fsfilter&1),
		'done'	:bool(fsfilter&2),
		'draft'	:bool(fsfilter&4),
		'onway'	:bool(fsfilter&8),
	})
	#queryset = __set_filter_state(queryset, fsfilter)
	# 3. go
	#if not request.user.is_superuser:
	#	queryset = queryset.filter(assign=request.user)
	return  object_list (
		request,
		queryset = queryset,
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'bills/list.html',
		extra_context = {
			'canadd': approver.canadd,
			'fsform': fsform,
		}
	)

@login_required
def	bill_filter_state(request):
	'''
	POST only
	* set filter iin cookie
	* redirect
	'''
	fsform = forms.FilterStateForm(request.POST)
	if fsform.is_valid():
		fsfilter = \
			int(fsform.cleaned_data['dead']) * 1 | \
			int(fsform.cleaned_data['done']) * 2 | \
			int(fsform.cleaned_data['draft'])  * 4 | \
			int(fsform.cleaned_data['onway'])  * 8
		#print 'Filter:', fsfilter
		request.session[FSNAME] = fsfilter
	return redirect('bills.views.bill_list')

def	__pdf2png(self, src_path, thumb_template, pages):
	for page in range(pages, 10):
		img = Wand_Image(filename = src_path + '[%d]' % page, resolution=(150,150))
		#print img.size
		if (img.colorspace != 'gray'):
			img.colorspace = 'gray'		# 'grey' as for bw as for grey (COLORSPACE_TYPES)
		img.format = 'png'
		#img.resolution = (300, 300)
		img.save(filename = thumb_template % page)

def	__pdf2png2(self, src_path, thumb_template, pages):
	arglist = ["gs",
		"-dBATCH",
		"-dNOPAUSE",
		"-sOutputFile=%s" % thumb_template,
		"-sDEVICE=pnggray",
		"-r150",
		src_path]
	sp = subprocess.Popen(args=arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	sp.communicate()

def	__convert_img(file):
	'''
	Convert image
	@param img:django.core.files.uploadedfile.InMemoryUploadedFile
	@return list of output filepaths
	'''
	retvalue = list()
	filename = file.name
	filemime = file.content_type
	src_filename = default_storage.save(file.name, ContentFile(file.read()))	# unicode
	src_path = os.path.join(settings.MEDIA_ROOT, filename)
	basename = filename.rsplit('.', 1)[0]
	dirname = settings.MEDIA_ROOT
	if (filemime == 'image/png'):
		img = PIL_Image.open(src_path)
		if (img.mode not in set(['1', 'L'])):	# [paletted ('P')], bw, grey
			img.convert('L').save(src_path)
		retvalue.append(filename)
	elif (filemime == 'image/jpeg'):
		img = PIL_Image.open(src_path)
		dst_filename = basename + '.png'
		img.convert('L').save(os.path.join(settings.MEDIA_ROOT, dst_filename), 'PNG')
		os.unlink(src_path)
		retvalue.append(dst_filename)
	elif (filemime == 'image/tiff'):
		img = PIL_Image.open(src_path)
		for i in range(9):
			try:
				img.seek(i)
				if (img.mode in set(['1','L'])):
					thumb = img
				else:
					thumb = img.convert('L')
				dst_filename = '%s-%d.png' % (basename, i+1)
				thumb.save(os.path.join(settings.MEDIA_ROOT, dst_filename), 'PNG')
				retvalue.append(dst_filename)
			except EOFError:
				break
		os.unlink(src_path)
	elif (filemime == 'application/pdf'):
		#pages = PdfFileReader(file(src_path, 'rb')).getNumPages()
		pages = min(9, len(PdfReader(file(src_path, 'rb')).pages))
		self.__pdf2png2(src_path, thumb_template, pages)
	return retvalue

def	__update_fileseq(f, fileseq):
	for file in __convert_img(f):
		myfile = File(file=SimpleUploadedFile(file, default_storage.open(file).read()))
		myfile.save()
		default_storage.delete(file)
		fileseq.add_file(myfile)

@login_required
def	bill_add(request):
	'''
	Add new (draft) bill
	ACL: Исполнитель
	- add Bill
	- add Route to them
	- convert image
	- add images into fileseq
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
			__update_fileseq(request.FILES['file'], fileseq)
			# 3. bill at all
			bill = models.Bill(
				fileseq		= fileseq,
				project		= form.cleaned_data['project'],
				depart		= form.cleaned_data['depart'],
				supplier	= form.cleaned_data['supplier'],
				assign		= approver,
				rpoint		= None,
				done		= None,
			)
			bill.save()
			# 4. add route
			std_route1 = [
				(2, models.Approver.objects.get(pk=13), 1, 'Ok'),	# начОМТС
				(3, form.cleaned_data['approver'], 1, 'Ok'),		# Руководитель
				(4, None, 1, 'Ok'),					# Директор
				(5, models.Approver.objects.get(pk=3), 1, 'Ok'),	# Гендир
				(6, models.Approver.objects.get(pk=4), 2, 'Oплачено'),	# Бухгалтер
			]
			for i, r in enumerate(std_route1):
				bill.route_set.add(
					models.Route(
						bill	= bill,
						order	= i+1,
						role	= models.Role.objects.get(pk=r[0]),
						approve	= r[1],
						state	= models.State.objects.get(pk=r[2]),
						action	= r[3],
					),
				)
			#bill = form.save(commit=False)
			return redirect('bills.views.bill_view', bill.pk)
	else:
		form = forms.BillAddForm()
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {'form': form,}))

@login_required
def	bill_edit(request, id):
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
			if (bill.project != form.cleaned_data['project']):
				bill.project = form.cleaned_data['project']
				tosave = True
			if (bill.depart != form.cleaned_data['depart']):
				bill.depart = form.cleaned_data['depart']
				tosave = True
			if (bill.supplier != form.cleaned_data['supplier']):
				bill.supplier = form.cleaned_data['supplier']
				tosave = True
			if (tosave):
				bill.save()
			# 2. update approver (if required)
			special = bill.route_set.get(order=2)
			if (special.approve != form.cleaned_data['approver']):
				special.approve = form.cleaned_data['approver']
				special.save()
			# 3. update image
			file = request.FILES.get('file', None)
			if (file):
				fileseq = bill.fileseq
				fileseq.clean_children()
				__update_fileseq(file, fileseq)
			return redirect('bills.views.bill_view', bill.pk)
	else:
		form = forms.BillEditForm(initial={
			'project':	bill.project,
			'depart':	bill.depart,
			'supplier':	bill.supplier,
			'approver':	bill.route_set.get(order=2).approve,
			#'approver':	6,
		})
	return render_to_response('bills/form.html', context_instance=RequestContext(request, {
		'form': form,
		'object': bill,
	}))

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
	approver = models.Approver.objects.get(user=user)
	bill = models.Bill.objects.get(pk=int(id))
	bill_state_id = bill.get_state_id()
	form = None
	err = ''
	if (request.method == 'POST'):
		if (request.POST['resume'] in set(['accept', 'reject'])) and (\
		   ((approver == bill.assign) and (bill_state_id == 1)) or\
		   ((approver == bill.approve) and (bill_state_id == 2)) \
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
						print route_list
						if (bill.isgood == False):			# 1st (draft)
							#print "1st"
							bill.isgood = True
							bill.approve = route_list[0]
						elif (approver == route_list[len(route_list)-1]):		# last
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
		## root | (assignee & Draft)
		'canedit':	(user.is_superuser or ((bill_state_id == 1) and (bill.assign == approver))),
		## root | (assignee & (Draft|Rejected)==bad)
		'candel':	(user.is_superuser or (((bill_state_id == 1) or (bill_state_id == 4)) and (bill.assign == approver))),
		## (assignee & Draft) | (approver & OnWay)
		'canaccept': (((bill_state_id == 1) and (bill.assign == approver)) or ((bill_state_id == 2) and (bill.rpoint.approve == approver))),
		#'pagelist': range(bill.pages),
		'err': err
	}))
'''
@login_required
def	bill_get(request, id):
	bill = models.Bill.objects.get(pk=int(id))
	response = HttpResponse(mimetype=bill.mime)
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = '; filename=' + bill.name.encode('utf-8')
	response.write(open(bill.get_path()).read())
	return response
'''
@login_required
def	bill_delete(request, id):
	'''
	Delete bill
	ACL: (root|assignee) & (Draft|Rejected (bad))
	'''
	bill = models.Bill.objects.get(pk=int(id))
	if (not request.user.is_superuser) and (\
	   (bill.assign.user.pk != request.user.pk) or\
	   (bill.done != None) or\
	   (bill.rpoint != None)):
		return redirect('bills.views.bill_view', bill.pk)
	fileseq = bill.fileseq
	bill.delete()
	fileseq.purge()
	return redirect('bills.views.bill_list')

