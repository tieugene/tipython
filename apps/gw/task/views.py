# -*- coding: utf-8 -*-
'''
lansite.gw.task.views.py
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext

# 2. python
from datetime import datetime

# 3. my
from models import *
from forms import *

# 4. siblings
from gw.bits.forms import UserListForm

def	__handle_sortfilter(request, user, viewname):
	'''
	Handle sort and filter set params of url
	@param user:User - user
	@param viewname:str - view name
	url params:
		#user == user
		#form == const
		 a == action
		 o == object
		 v == value
		sort: a=s&
			[o=*&]v=0			# remove sorting
			o=<column>&v=1|-1		# sort
		filter:
			a=f&
				v=0			# remove all filters
				o=<column>&v=0		# remove column filters
				o=<column>&v=<value>	# set filter
	'''
	p = dict()
	for i in ('a', 'o', 'v'):
		v = request.GET.get(i, None)
		if v:
			p[i] = v
	# 2. save new settings
	if (p):
		# FIXME: check params - must be 2 or 3 and defined
		if (p['a'] == 's'):			# sorting: a column only => change sort setting
			if (p['v'] == '0'):		# remove sorting
				UserSetting.objects.filter(user=user, form=viewname, action='sort').delete()
			else:				# set new sorting
				UserSetting.objects.cu_ufa(user=user, form=viewname, action='sort', object=p['o'], value = p['v'])
		if (p['a'] == 'f'):			# filtering
			if (p['v'] == '*'):	
				if (p.has_key('o')):	# remove a column filter
					UserSetting.objects.filter(user=user, form=viewname, action='filter', object=p['o']).delete()
				else:			# remove all filters
					UserSetting.objects.filter(user=user, form=viewname, action='filter').delete()
			else:
				UserSetting.objects.cu_ufao(user=user, form=viewname, action='filter', object=p['o'], value = p['v'])

def	__mkdefpd(data, sort_o, sort_v):
	'''
	Make default pulldown menus (Sort up, Sort down)
	'''
	head = list()
	for name, id in data:
		if (sort_o == id):
			if (sort_v == 2):
				name = u'&uarr;' + name
			else:
				name = u'&darr;' + name
		head.append({
			'id':		id,
			'name':		name,
			'title':	'',
			'menu':		[
				{ 'name': 'Sort up', 'url': '?a=s&o=%s&v=2' % id, 'type': 0},
				{ 'name': 'Sort down', 'url': '?a=s&o=%s&v=1' % id, 'type': 0},
			],
			})
	return head

def	task_list(request):
	s_form = 'task_list'
	user = User.objects.get(pk=request.user.id)
	__handle_sortfilter(request, user, s_form)
	item_list = Task.objects.all()
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		item_list = item_list.order_by(s)
	head = __mkdefpd((
		(u'Тип', 'type'),
		(u'Категория', 'category'),
		(u'Тема', 'subject'),
		(u'Создано', 'created'),
		(u'Автор', 'author'),
		(u'Исполнитель', 'assignee'),
		(u'Срок', 'deadline'),
		(u'Состояние', 'state'),
	), sort_o, sort_v)
	return render_to_response('gw/task/task_list.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задания',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('gw.views.assign_add'), 'type': 0},
					{ 'name': 'Отметить как выполненные', 'url': '#', 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Убрать фильтры', 'url': '?a=f&v=*', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head,
		},
	}))

def	task_add(request):
	pass

def	task_view(request, item_id):
	# user_type = ContentType.objects.get_for_model(User)
	cid = Task.objects.get(pk=item_id).getclassid()
	if (cid == 1):
		v = 'gw.views.todo_view'
	if (cid == 2):
		v = 'gw.views.assign_view'
	return HttpResponseRedirect(reverse(v, kwargs = {'item_id': item_id}))

def	task_edit(request, item_id):
	pass

def	task_del(request, item_id):
	pass

def	task_done(request, item_id):
	pass

def	todocat_list(request):
	s_form = 'todocat_list'
	user = User.objects.get(pk=request.user.id)	# aka author
	__handle_sortfilter(request, user, s_form)
	item_list = ToDoCat.objects.filter(author=user)
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		item_list = item_list.order_by(s)
	head = __mkdefpd((
		(u'Наименование', 'name'),
	), sort_o, sort_v)
	return render_to_response('gw/task/todocat_list.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Категории',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('gw.views.todocat_add'), 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head[0],
		},
	}))

def	todocat_add(request):
	if request.method == 'POST':
		form = ToDoCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.save()
			return HttpResponseRedirect(reverse('gw.views.todo_list'))
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todocat_view(request, item_id):
	return render_to_response('gw/task/todocat_view.html', context_instance=RequestContext(request, {'item': ToDoCat.objects.get(pk=item_id)}))

def	todocat_edit(request, item_id):
	item = ToDoCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('gw.views.todo_list'))
	else:	# GET
		form = ToDoCatForm(instance=item)
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

def	todocat_del(request, item_id):
	ToDoCat.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.todo_list'))

def	todocat_add_todo(request, item_id):
	cat = ToDoCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoOfCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.category = cat
			item.save()
			return HttpResponseRedirect(reverse('gw.views.todocat_view', kwargs = {'item_id': cat.id}))
	else:	# GET
		form = ToDoOfCatForm()
	return render_to_response('gw/task/todo_edt.html', context_instance=RequestContext(request, {'form': form}))

def	todo_list(request):
	s_form = 'todo_list'
	user = User.objects.get(pk=request.user.id)	# aka author
	# 1. get and save params
	__handle_sortfilter(request, user, s_form)
	# 2. prepare data
	item_list = ToDo.objects.filter(author=user)
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	# 3. sort
	if s:
		item_list = item_list.order_by(s)
	# 4. filter
	for f in UserSetting.objects.filter(user=user, form=s_form, action='filter'):
		o = f.object
		v = f.value
		if o == 'category':
			item_list = item_list.filter(category__id=int(v))
		if o == 'done':
			item_list = item_list.filter(done=bool(int(v)))
	# 5. prepare menus
	head = __mkdefpd((
		(u'Категория', 'category'),
		(u'Тема', 'subject'),
		(u'Создано', 'created'),
		(u'Срок', 'deadline'),
		(u'&radic;', 'done'),
	), sort_o, sort_v)
	head[0]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': [
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=category&v=*'},
		]},
	)
	for cat in ToDoCat.objects.filter(author=user):
		head[0]['menu'][2]['url'].append({'name': cat.name, 'url': '?a=f&o=category&v=%d' % cat.id})
	head[4]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=done&v=*'},
			{'name': u'Done', 'url': '?a=f&o=done&v=1'},
			{'name': u'Undone', 'url': '?a=f&o=done&v=0'},
		)},
	)
	# x. lets go
	return render_to_response('gw/task/todo_list.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задачи',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('gw.views.todo_add'), 'type': 0},
					{ 'name': 'Отметить как выполненные', 'url': '#', 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Убрать фильтры', 'url': '?a=f&v=*', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'cb': {
				'id':		'cb',
				'name':		'',
				'title':	'',
				'menu':		(
					{ 'name': 'Все', 'url': '#', 'type': 0},
					{ 'name': 'Ни одного', 'url': '#', 'type': 0},
					{ 'name': 'Инвертировать', 'url': '#', 'type': 0},
				),
			},
			'head':	head,
		},
	}))

def	todo_add(request):
	if request.method == 'POST':
		form = ToDoForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.created = datetime.now()
			item.save()
			return HttpResponseRedirect(reverse('gw.views.todo_list'))
	else:	# GET
		form = ToDoForm()
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todo_view(request, item_id):
	return render_to_response('gw/task/todo_view.html', context_instance=RequestContext(request, {'item': ToDo.objects.get(pk=item_id)}))

def	todo_edit(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('gw.views.todo_view', kwargs={'item_id': item.id}))
	else:	# GET
		form = ToDoForm(instance=item)
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todo_del(request, item_id):
	ToDo.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.todo_list'))

def	todo_done(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	item.done = True
	item.save()
	return HttpResponseRedirect(reverse('gw.views.todo_list'))

def	assigncat_list(request):
	s_form = 'assigncat_list'
	user = User.objects.get(pk=request.user.id)	# aka author
	__handle_sortfilter(request, user, s_form)
	item_list = AssignCat.objects.all()
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		item_list = item_list.order_by(s)
	head = __mkdefpd((
		(u'Наименование', 'name'),
	), sort_o, sort_v)
	return render_to_response('gw/task/assigncat_list.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Категории',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('gw.views.assigncat_add'), 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head[0],
		},
	}))

def	assigncat_add(request):
	if request.method == 'POST':
		form = AssignCatForm(request.POST)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('gw.views.assign_list'))
	else:	# GET
		form = AssignCatForm()
	return render_to_response('gw/task/assigncat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assigncat_view(request, item_id):
	return render_to_response('gw/task/assigncat_view.html', context_instance=RequestContext(request, {'item': AssignCat.objects.get(pk=item_id)}))

def	assigncat_edit(request, item_id):
	item = AssignCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = AssignCatForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('gw.views.assign_list'))
	else:	# GET
		form = AssignCatForm(instance=item)
	return render_to_response('gw/task/assigncat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

def	assigncat_del(request, item_id):
	AssignCat.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.assign_list'))

def	assign_list(request):
	s_form = 'assign_list'
	user = User.objects.get(pk=request.user.id)	# aka author
	__handle_sortfilter(request, user, s_form)
	item_list = Assign.objects.filter(Q(author=user) | Q(assignee=user))
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		item_list = item_list.order_by(s)
	for f in UserSetting.objects.filter(user=user, form=s_form, action='filter'):
		o = f.object
		v = int(f.value)
		if o == 'category':
			item_list = item_list.filter(category__id=v)
		if o == 'author':
			if (v == 0):
				item_list = item_list.exclude(author__id=v)
			else:
				item_list = item_list.filter(author__id=v)
		if o == 'assignee':
			if (v == -1):
				item_list = item_list.filter(assignee=None)
			elif (v == 0):
				item_list = item_list.exclude(assignee__id=v)
			else:
				item_list = item_list.filter(assignee__id=v)
		if o == 'done':
			item_list = item_list.filter(done=bool(v))
		if o == 'read':
			item_list = item_list.filter(read=bool(v))
	# 5. prepare menus
	head = __mkdefpd((
		(u'Категория', 'category'),
		(u'Тема', 'subject'),
		(u'Создано', 'created'),
		(u'Автор', 'author'),
		(u'Исполнитель', 'assignee'),
		(u'Важность', 'importance'),
		(u'Срок', 'deadline'),
		(u'Сделано', 'done'),
		(u'Принято', 'read'),
	), sort_o, sort_v)
	head[0]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': [
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=category&v=*'},
		]},
	)
	for cat in AssignCat.objects.all():
		head[0]['menu'][2]['url'].append({'name': cat.name, 'url': '?a=f&o=category&v=%d' % cat.id})
	head[3]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=author&v=*'},
			{'name': u'&lt;Я&gt', 'url': '?a=f&o=author&v=%d' % user.id},
			{'name': u'&lt;Не я&gt', 'url': '?a=f&o=author&v=0'},
		)},
	)
	for i in GwUser.objects.exclude(user=user):
		head[3]['menu'][2]['url'].append({'name': i.user.username, 'url': '?a=f&o=author&v=%d' % i.id})
	head[4]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=assignee&v=*'},
			{'name': u'&lt;Мне&gt', 'url': '?a=f&o=assignee&v=%d' % user.id},
			{'name': u'&lt;Не мне&gt', 'url': '?a=f&o=assignee&v=0'},
			{'name': u'&lt;Никому&gt', 'url': '?a=f&o=assignee&v=-1'},
		)},
	)
	for i in GwUser.objects.exclude(user=user):
		head[4]['menu'][2]['url'].append({'name': i.user.username, 'url': '?a=f&o=assignee&v=%d' % i.id})
	head[7]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=done&v=*'},
			{'name': u'Done', 'url': '?a=f&o=done&v=1'},
			{'name': u'Undone', 'url': '?a=f&o=done&v=0'},
		)},
	)
	head[8]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=read&v=*'},
			{'name': u'Принято', 'url': '?a=f&o=read&v=1'},
			{'name': u'Непринято', 'url': '?a=f&o=read&v=0'},
		)},
	)
	# x. lets go
	return render_to_response('gw/task/assign_list.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задания',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('gw.views.assign_add'), 'type': 0},
					{ 'name': 'Отметить как выполненные', 'url': '#', 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Убрать фильтры', 'url': '?a=f&v=*', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head,
		},
	}))

def	assign_add(request):
	'''
	Create action
	'''
	if request.method == 'POST':
		form = AssignForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.created = datetime.now()
			item.save()
			return HttpResponseRedirect(reverse('gw.views.assign_list'))
	else:	# GET
		form = AssignForm()
	return render_to_response('gw/task/assign_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assign_view(request, item_id):
	'''
	Main dispatcher.
	Actions:
		* New: assignee:Accept
		* Accepted: assignee:Route; MkDep; Invalid; Duplicate; Done
		* Completed: author:Approve; author:ReOpen
		* Approved: author:ReOpen
	'''
	return render_to_response('gw/task/assign_view.html', context_instance=RequestContext(request, {
		'item': Assign.objects.get(pk=item_id),
		'form1': UserListForm(),
		'form2': LineCommentForm(),
		'form3': AssignDupForm(),
	}))

def	assign_edit(request, item_id):
	item = Assign.objects.get(pk=item_id)
	if request.method == 'POST':
		form = AssignForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('gw.views.assign_list'))
	else:	# GET
		form = AssignForm(instance=item)
	return render_to_response('gw/task/assign_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assign_del(request, item_id):
	item = Assign.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('gw.views.assign_list'))

def	assign_route(request, item_id):
	'''
	Route action: set assignee to new; set state to new;
	'''
	item = Assign.objects.get(pk=item_id)
	if request.method == 'POST':
		if request.POST['user']:
			uid = int(request.POST['user'])
			if (uid != request.user.id):
				item.assignee = GwUser.objects.get(pk=uid)
				item.read = False
				item.save()
				__log_it(request, item, CHANGE, u'Routed to %s' % item.assignee)
				return HttpResponseRedirect(reverse('gw.views.assign_list'))
	return assign_view(request, item_id)

def	assign_invalid(request, item_id):
	'''
	Invalid action: set state to done, w/ comments
	'''
	# FIXME:
	#__log_it(request, item, CHANGE, u'Invalid: %s' % item.assignee)
	return assign_done(request, item_id)

def	assign_duped(request, item_id):
	'''
	Duplicate action set state to done, w/ comments
	'''
	# FIXME:
	#__log_it(request, item, CHANGE, u'Duplicated: %s' % item.assignee)
	return assign_done(request, item_id)

def	assign_accept(request, item_id):
	'''
	Accept action: set state to done
	'''
	item = Assign.objects.get(pk=item_id)
	item.read = True
	item.save()
	__log_it(request, item, CHANGE, u'Accepted')
	return HttpResponseRedirect(reverse('gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_done(request, item_id):
	'''
	Done action
	'''
	item = Assign.objects.get(pk=item_id)
	item.done = True
	item.read = False
	item.save()
	__log_it(request, item, CHANGE, u'Done')
	return HttpResponseRedirect(reverse('gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_approve(request, item_id):
	'''
	Approve action
	'''
	item = Assign.objects.get(pk=item_id)
	__log_it(request, item, CHANGE, u'Approved')
	return assign_accept(request, item_id)

def	assign_reopen(request, item_id):
	'''
	ReOpen action
	'''
	item = Assign.objects.get(pk=item_id)
	item.done = False
	item.read = False
	item.save()
	__log_it(request, item, CHANGE, u'Reopened')
	return HttpResponseRedirect(reverse('gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_mksub(request, item_id):
	'''
	Create subaction
	'''
	if request.method == 'POST':
		form = AssignForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.created = datetime.now()
			item.save()
			__log_it(request, item, ADDITION)
			master = Assign.objects.get(pk=item_id)
			SubObject(master = master, slave = item).save()
			return HttpResponseRedirect(reverse('gw.views.assign_view', kwargs={'item_id': master.id}))
	else:	# GET
		form = AssignForm()
	return render_to_response('gw/task/assign_edt.html', context_instance=RequestContext(request, {'form': form}))

def	assign_history(request, item_id):
	return render_to_response('gw/task/assign_history.html', context_instance=RequestContext(request, {'item_list': LogEntry.objects.filter(object_id = item_id).order_by('action_time')}))
