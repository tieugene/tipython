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
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.views.generic.simple import direct_to_template

# 2. python
from datetime import datetime, date, time, timedelta

# 3. 3rd party
from icalendar import Calendar, Todo, UTC

# 4. my
from models import *
from forms import *

# 5. siblings
from gw.bits.forms import UserListForm

'''
Removed:
task_done (empty)
todo_addsub:	Add sub todo
todo_onsub:	Make todo as child of
todo_unsub:	Get todo from children of
assign_invalid:	Invalid action: set state to done, w/ comments
assign_duped:	Duplicate action set state to done, w/ comments
'''

datetype = type(date)
datetimetype = type(datetime)

@login_required
def	__handle_sortfilter(request, user, viewname):
	'''
	Handle sort and filter set params of url
	@param user:GwUser - user
	@param viewname:str - view name
	url params:
		#user == user
		#form == const
		 a == action
		 o == object
		 v == value
		sort: a=s&
			[o=*&]v=0			# remove [all] sorting[s]
			o=<column>&v=1|-1		# sort up/down
		filter:
			a=f&
				v=*			# remove all filters
				o=<column>&v=*		# remove column filters
				o=<column>&v=<value>	# set filter
		column: a=c&
				v=1			# show all columns
				o=<column>&v=0|1	# hide|show column
	'''
	p = dict()
	for i in ('a', 'o', 'v'):
		v = request.GET.get(i, None)
		if v:
			p[i] = v
	# 2. save new settings
	if (p):
		user = user.user
		# FIXME: check params - must be 2 or 3 and defined
		if (p['a'] == 's'):			# sorting: a column only => change sort setting
			if (p['v'] == '0'):		# remove sorting
				UserSetting.objects.filter(user=user, form=viewname, action='sort').delete()
			else:				# set new sorting
				UserSetting.objects.cu_ufa(user=user, form=viewname, action='sort', object=p['o'], value = p['v'])
		elif (p['a'] == 'f'):			# filtering
			if (p['v'] == '*'):	
				if (p.has_key('o')):	# remove a column filter
					UserSetting.objects.filter(user=user, form=viewname, action='filter', object=p['o']).delete()
				else:			# remove all filters
					UserSetting.objects.filter(user=user, form=viewname, action='filter').delete()
			else:
				UserSetting.objects.cu_ufao(user=user, form=viewname, action='filter', object=p['o'], value = p['v'])
		elif (p['a'] == 'c'):			# columns
			if (p.has_key('o')):		# a column
				if (p['v'] == '1'):
					UserSetting.objects.filter(user=user, form=viewname, action='column', object=p['o']).delete()
				else:			# remove all filters
					UserSetting.objects.cu_ufao(user=user, form=viewname, action='column', object=p['o'], value = p['v'])
			else:
				if (p['v'] == '1'):
					UserSetting.objects.filter(user=user, form=viewname, action='column').delete()

@login_required
def	__mkdefpd(data, sort_o, sort_v):
	'''
	Make default pulldown menus (Sort up, Sort down)
	'''
	head = list()
	#head[0]['menu'][2]['url']
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

@login_required
def	category_index(request):
	s_form = 'todocat_list'
	user = GwUser.objects.get(pk=request.user.id)	# aka author
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

@login_required
def	category_add(request):
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

@login_required
def	category_detail(request, item_id):
	return render_to_response('gw/task/todocat_view.html', context_instance=RequestContext(request, {'item': ToDoCat.objects.get(pk=item_id)}))

@login_required
def	category_edit(request, item_id):
	item = ToDoCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('gw.views.todo_list'))
	else:	# GET
		form = ToDoCatForm(instance=item)
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

@login_required
def	category_del(request, item_id):
	ToDoCat.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.todo_list'))

@login_required
def	category_add_todo(request, item_id):
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

@login_required
def	task_index(request):
	'''
	FIXME: handle settings and redirect to todo, contacts etc
	'''
	return render_to_response('gw/task/index.html', context_instance=RequestContext(request))

@login_required
def	task_index_all(request):
	'''
	FIXME: handle settings and redirect to todo, contacts etc
	'''
	return redirect('gw.views.todo_index')
	s_form = 'task_list'
	user = GwUser.objects.get(pk=request.user.id)
	__handle_sortfilter(request, user, s_form)
	item_list = Task.objects.all()
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		item_list = item_list.order_by(s)
	head = __mkdefpd((
		(u'Тип', 'type'),
		(u'Автор', 'user'),
		(u'Создано', 'created'),
		(u'Изменено', 'updated'),
		(u'Тема', 'summary'),
		(u'Состояние', 'status'),
		(u'Видимость', 'restriction'),
	), sort_o, sort_v)
	return render_to_response('gw/task/task_index.html', context_instance=RequestContext(request, {
		'item_list': item_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задачи',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить Задание', 'url': reverse('gw.views.todo_add'), 'type': 0},
					{ 'name': 'Добавить Событие', 'url': reverse('gw.views.event_add'), 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Убрать фильтры', 'url': '?a=f&v=*', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head,
		},
	}))

@login_required
def	task_detail(request, item_id):
	# user_type = ContentType.objects.get_for_model(User)
	cid = Task.objects.get(pk=item_id).getclassid()
	if (cid == 1):
		v = 'gw.views.todo_view'
	if (cid == 2):
		v = 'gw.views.assign_view'
	return HttpResponseRedirect(reverse(v, kwargs = {'item_id': item_id}))

@login_required
def	task_del(request, item_id):
	pass

@login_required
def	task_edit(request, item_id):
	pass

@login_required
def	ical_index(request):
	s_form = 'ical_list'
	user = GwUser.objects.get(pk=request.user.id)	# aka author
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
		(u'Тип', 'type'),
		(u'Автор', 'user'),
		(u'Создано', 'created'),
		(u'Изменено', 'created'),
		(u'Тема', 'summary'),
		(u'Состояние', 'status'),
		(u'Видимость', 'restriction'),
		# ----
		(u'Исполнитель', 'attendee'),
		(u'Начало', 'start'),
		(u'Длительность', 'duration'),
		(u'Место', 'location'),
		(u'Важность', 'priority'),
		(u'URL', 'URL'),
	), sort_o, sort_v)
	# filter on category
	head[0]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': [
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=summary&v=*'},
		]},
	)
	for cat in AssignCat.objects.all():
		head[0]['menu'][2]['url'].append({'name': cat.name, 'url': '?a=f&o=summary&v=%d' % cat.id})
	# filter on user
	head[3]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=user&v=*'},
			{'name': u'&lt;Я&gt', 'url': '?a=f&o=user&v=%d' % user.id},
			{'name': u'&lt;Не я&gt', 'url': '?a=f&o=user&v=0'},
		)},
	)
	for i in GwUser.objects.exclude(user=user):
		head[3]['menu'][2]['url'].append({'name': i.user.username, 'url': '?a=f&o=author&v=%d' % i.id})
	# filter on attendee
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
	# filter on status
	head[7]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=done&v=*'},
			{'name': u'Done', 'url': '?a=f&o=done&v=1'},
			{'name': u'Undone', 'url': '?a=f&o=done&v=0'},
		)},
	)
	# filter on status
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

def	__getneedcats(user, app):
	'''
	return Categories for this user and app
	'''
	cat_list = Category.objects.all()
	return (cat_list.filter(app=None) | cat_list.filter(app=app)) & (cat_list.filter(user=None) | cat_list.filter(user=user))

@login_required
def	todo_index(request):
	s_form = 'todo_list'
	user = GwUser.objects.get(pk=request.user.id)	# aka author
	# 1. get and save params (of URL - into settings)
	__handle_sortfilter(request, user, s_form)
	# 2. prepare data
	item_list = vToDo.objects.all()
	# my or for me or public
	item_list = item_list.filter(user=user) | item_list.filter(attendee=user) | item_list.filter(restriction=1)
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)	# ..., s: sort order
	# ... columns to show
	columns_form = ColumnsForm()
	hcol_dict = dict()
	for c in UserSetting.objects.filter(user=user, form=s_form, action='column', value='0'):
		hcol_dict[c.object] = True
		columns_form.fields[c.object].initial = False
	item_head = list()
	for k, v in (
		(u'Автор', 'user'),		# Task
		(u'Создано', 'created'),
		(u'Изменено', 'updated'),
		(u'Тема', 'summary'),
		(u'Состояние', 'status'),
		(u'Видимость', 'restriction'),
		(u'Категории', 'categories'),
		(u'Исполнитель', 'attendee'),	# iCal
		(u'Начало', 'start'),
		(u'Длительность', 'duration'),
		(u'Приоритет', 'priority'),
		(u'До', 'due'),
		(u'Завершено', 'completed'),
		(u'%', 'percent'),
	):
		if v not in hcol_dict:
			item_head.append(k)
	# 3. sort
	sort_form = SortForm()
	if s:
		if s.startswith('-'):
			sort_form.fields[s[1:]].initial = 1
		else:
			sort_form.fields[s].initial = 2
		item_list = item_list.order_by(s)
	# 4. filter (user, status, restriction; attendee, priority)
	filter_form = FilterForm()
	#for u in GwUser.objects.all():
	#	filter_form.fields['user'].choices.append((u.user.id, u.user.username))
	#	filter_form.fields['attendee'].choices.append((u.user.id, u.user.username))
	current_cat = None	# current selected category
	for f in UserSetting.objects.filter(user=user, form=s_form, action='filter'):
		# FIXME: *
		o = f.object
		v = f.value
		if (o not in ('categories', 'user', 'attendee')):
			filter_form.fields[o].initial = int(v)
		if o == 'user':
			item_list = item_list.filter(user=int(v))
			filter_form.fields[o].initial = GwUser.objects.get(pk=int(v))
		if o == 'status':
			item_list = item_list.filter(status=int(v))
		if o == 'restriction':
			item_list = item_list.filter(restriction=int(v))
		if o == 'attendee':
			item_list = item_list.filter(attendee__user__id=int(v))
			filter_form.fields[o].initial = GwUser.objects.get(pk=int(v))
		if o == 'priority':
			if v == '0':
				item_list = item_list.filter(priority=None)
			else:
				item_list = item_list.filter(priority=int(v))
		if o == 'categories':
			item_list = item_list.filter(categories=int(v))
			current_cat = int(v)
	# 5. prepare menus
	# x. let's go
	cat_list = __getneedcats(user, ContentType.objects.get_for_model(vToDo))
	return render_to_response('gw/task/todo_index.html', context_instance=RequestContext(request, {
		'cat_list': cat_list,		# Query of my categories
		'current_cat': current_cat,	# int - id of selected category
		'hcol_dict': hcol_dict,
		'item_head': item_head,
		'columns_form': columns_form,
		'sort_form': sort_form,
		'filter_form': filter_form,
		'item_list': item_list,		# Query of vToDo
	}))

@login_required
def	todo_index_setcolumns(request):
	form = ColumnsForm(request.POST)
	if form.is_valid():
		cols = form.getData()
		user = User.objects.get(pk=request.user.id)
		UserSetting.objects.filter(user=user, form='todo_list', action='column').delete()
		for k, v in cols.iteritems():
			if not v:
				UserSetting.objects.create(user=user, form='todo_list', action='column', object=k, value='0')
	return redirect('gw.views.todo_index')

@login_required
def	todo_index_setsort(request):
	form = SortForm(request.POST)
	if form.is_valid():
		sorts = form.getData()
		user = User.objects.get(pk=request.user.id)
		UserSetting.objects.filter(user=user, form='todo_list', action='sort').delete()
		for k, v in sorts.iteritems():
			if v:
				UserSetting.objects.create(user=user, form='todo_list', action='sort', object=k, value=v)
	return redirect('gw.views.todo_index')

@login_required
def	todo_index_setfilter(request):
	form = FilterForm(request.POST)
	if form.is_valid():
		filters = form.getData()
		user = User.objects.get(pk=request.user.id)
		UserSetting.objects.filter(user=user, form='todo_list', action='filter').delete()
		for k, v in filters.iteritems():
			if v:
				UserSetting.objects.create(user=user, form='todo_list', action='filter', object=k, value=v)
	else:
		print "Invalid form"
	return redirect('gw.views.todo_index')

@login_required
def	todo_add(request):
	form = ToDoForm(request.POST or None)
	if form.is_valid():
		item = form.save(commit=False)
		item.user = GwUser.objects.get(pk=request.user.id)
		item.created = datetime.now()
		item.updated = datetime.now()
		item.save()
		form.save_m2m()
		return HttpResponseRedirect(reverse('gw.views.todo_index'))
	return direct_to_template(request, 'gw/task/todo_edit.html', {'form': form})

@login_required
def	todo_detail(request, item_id):
	item = vToDo.objects.get(pk=item_id)
	xq = item.taskcat_set.all().values_list('cat__id', flat=True)
	q = __getneedcats(user = GwUser.objects.get(pk=request.user.id), app = ContentType.objects.get_for_model(vToDo)).exclude(id__in=xq)
	if (q):
		form = ChoiceForm(q = q)
	else:
		form = None
	return render_to_response('gw/task/todo_detail.html', context_instance=RequestContext(request, {
		'item': item,
		'form': form,
	}))

@login_required
def	todo_edit(request, item_id):
	item = vToDo.objects.get(pk=item_id)
	form = ToDoForm(request.POST or None, instance=item)
	if form.is_valid():
		item = form.save(commit=False)
		item.updated = datetime.now()
		item = form.save()
		return HttpResponseRedirect(reverse('gw.views.todo_detail', kwargs={'item_id': item.id}))
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

@login_required
def	todo_del(request, item_id):
	vToDo.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.todo_index'))	# FIXME: next

@login_required
def	todo_done(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	item.done = True
	item.save()
	return HttpResponseRedirect(reverse('gw.views.todo_list'))

@login_required
def	todo_cat_add(request):
	'''
	Add new Category for ToDo list
	'''
	form = CategoryForm(request.POST or None)
	if form.is_valid():
		item = form.save(commit=False)
		if (form.cleaned_data['thisuser']):
			item.user = GwUser.objects.get(pk=request.user.id)
		else:
			item.user = None
		if (form.cleaned_data['thisapp']):
			item.app = ContentType.objects.get_for_model(vToDo)
		else:
			item.app = None
		item = form.save()
		return HttpResponseRedirect(reverse('gw.views.todo_index'))
	return direct_to_template(request, 'gw/task/todo_cat_edit.html', {'form': form})

@login_required
def	todo_cat_edit(request, item_id):
	'''
	Edit category in ToDo list
	'''
	item = Category.objects.get(pk=item_id)
	user = GwUser.objects.get(pk=request.user.id)
	app = ContentType.objects.get_for_model(vToDo)
	#print item.user == request.user, item.app == ContentType.objects.get_for_model(vToDo)
	#print item.user == user, item.app, ContentType.objects.get_for_model(vToDo)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance = item, initial = {'thisuser': item.user == user, 'thisapp': item.app == app})
		if form.is_valid():
			item = form.save(commit=False)
			if (form.cleaned_data['thisuser']):
				item.user = user
			else:
				item.user = None
			if (form.cleaned_data['thisapp']):
				item.app = app
			else:
				item.app = None
			item = form.save()
			return HttpResponseRedirect(reverse('gw.views.todo_index'))
	else:
		form = CategoryForm(instance = item, initial = {'thisuser': item.user == user, 'thisapp': item.app == app})
	return direct_to_template(request, 'gw/task/todo_cat_edit.html', {'form': form})

@login_required
def	todo_addcat(request, item_id):
	'''
	Add category to todo (in detail mode ?..)
	'''
	item = vToDo.objects.get(pk=item_id)
	form = ChoiceForm(Category.objects.all(), request.POST)
	if form.is_valid():
		TaskCat(task=item, cat=form.cleaned_data['item']).save()
	return HttpResponseRedirect(reverse('gw.views.todo_detail', kwargs={'item_id': int(item_id)}))

@login_required
def	todo_delcat(request, item_id):
	'''
	item_id - TaskCat
	'''
	tc = TaskCat.objects.get(pk=item_id)
	todo = tc.task
	tc.delete()
	return HttpResponseRedirect(reverse('gw.views.todo_detail', kwargs={'item_id': todo.id}))

@login_required
def	todo_cat_del(request, item_id):
	'''
	item_id - Category
	'''
	Category.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.todo_index'))

@login_required
def	todo_cat_del_selected(request):
	for i in set(map(int, request.POST.getlist('cat'))):
		Category.objects.get(pk=i).delete()
	return redirect('gw.views.todo_index')

@login_required
def	todo_ical_export(request):
	'''
	Type: iCalendar
	Mime: text/calendar
	Ext: ics
	#tpl = loader.get_template('gw/task/todo.ics')
	#response.write(tpl.render(Context({'item_list': item_list})).encode('utf-8'))
	'''
	user = GwUser.objects.get(pk=request.user.id)	# aka author
	response = HttpResponse(mimetype='text/calendar')
	response['Content-Disposition'] = '; filename=todo.ics'
	cal = Calendar()
	cal.add('prodid', '-//LanSite GroupWare//eap.su//')
	cal.add('version', '2.0')
	for item in vToDo.objects.filter(user=user):
		todo = Todo()
		# 1. Task
		#todo['created'] = item.created
		todo.add('created', item.created)
		todo.add('last-modified', item.updated)
		todo.add('summary', item.summary)
		todo.add('status', item.getstatusname())
		todo.add('class', item.getrestrictionname())
		todo.add('categories', item.getcategories())
		# 2. vCal
		if item.attendee:
			email = item.attendee.user.email
			if email:
				todo.add('attendee', 'MAILTO:%s' % email)
			email = user.user.email
			if email:
				todo.add('organizer', 'MAILTO:%s' % email)
		if item.description:
			todo.add('description', item.description)
		if item.start_d:
			if item.start_t:
				todo.add('dtstart', datetime.combine(item.start_d, item.start_t))
			else:
				todo.add('dtstart', item.start_d)
		if item.duration_d:
			if item.duration_t:
				todo.add('duration', timedelta(
					days=item.duration_d,
					hours=item.duration_t.hour,
					minutes=item.duration_t.minute,
					seconds=item.duration_t.second
				))
			else:
				todo.add('duration', timedelta(days=item.duration_d))
		if item.location:
			todo.add('location', item.location)
		if item.priority:
			todo.add('priority', item.priority)
		if item.URL:
			todo.add('URL', item.URL)
		# 3. vToDo
		if item.due_d:
			if item.due_t:
				todo.add('due', datetime.combine(item.due_d, item.due_t))
			else:
				todo.add('due', item.due_d)
		if item.completed:
			todo.add('completed', item.completed)
		if item.percent:
			todo.add('percent-complete', item.percent)
		cal.add_component(todo)
	response.write(cal.as_string())		# .encode('utf-8')
	return response

@login_required
def	__rawdt(dt):
	return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

@login_required
def	todo_ical_import(request):
	result = list()
	if (request.method == 'POST'):
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			cal = Calendar.from_string(file.read())
			user = GwUser.objects.get(pk=request.user.id)
			app = ContentType.objects.get_for_model(vToDo)
			mycats = __getneedcats(user, app)
			for cmp in cal.walk():
				cname = cmp.name
				if (cname == 'VTODO'):
					# TODO: attendee:MAILTO:user...@
					# 1. Task
					item = vToDo(user=user)
					item.created = __rawdt(cmp.decoded('created'))
					item.updated = __rawdt(cmp.decoded('last-modified'))
					item.summary = cmp.decoded('summary')
					item.status = VTODO_STATUS_REVERSE.get(cmp.decoded('status').upper(), None)
					item.restriction = RESTRICTION_REVERSE.get(cmp.decoded('class').upper(), None)
					# 2. vCal
					#item.attendee = cmp.decoded('attendee')
					attendee = cmp.decoded('attendee', None)
					if (attendee):
						users = GwUser.objects.filter(user__email=attendee).order_by('user__username')
						if users.count():
							item.attendee = users[0]
					item.description = cmp.decoded('description', None)
					start = cmp.decoded('dtstart', None)
					if (start):
						if type(start) == datetype:
							item.start_d = start.date
							item.start_t = start.time
						else:
							item.start_d = start
					duration = cmp.decoded('duration', None)
					if (duration):
						if (duration.days):
							item.duration_d = duration.days
						if (duration.seconds):
							item.duration_t = (datetime.min + timedelta(0, duration.seconds)).time()
					item.location = cmp.decoded('location', None)
					item.priority = cmp.decoded('priority', None)
					item.URL = cmp.decoded('URL', None)
					# 3. vToDo
					due = cmp.decoded('due', None)
					if (due):
						if type(due) == datetype:
							item.due_d = due.date
							item.due_t = due.time
						else:
							item.due_d = due
					item.completed = cmp.decoded('completed', None)
					item.percent = cmp.decoded('percent-complete', None)
					# x. That's all
					item.save()
					# y. No, not all...
					cats = cmp.decoded('categories', None)
					if cats:
						for c in cats.split(','):
							findcat = mycats.filter(name=c).order_by('user', 'app')	# FIXME: 1. user+app, 2. app, 3. user
							if (findcat.count()):
								TaskCat(task=item, cat=findcat[0]).save()
							else:
								cat = Category(name=c, user=user, app=app)
								cat.save()
								TaskCat(task=item, cat=cat).save()
			return HttpResponseRedirect(reverse('gw.views.todo_index'))
	else:
		form = FileUploadForm()
	return render_to_response('gw/task/todo_ical_upload.html', context_instance=RequestContext(request, {'form': form, 'result': result}))

@login_required
def	todo_del_selected(request):
	for i in set(map(int, request.POST.getlist('todo'))):
		vToDo.objects.get(pk=i).delete()
	return redirect('gw.views.todo_index')

@login_required
def	event_index(request):
	s_form = 'assign_list'
	user = GwUser.objects.get(pk=request.user.id)	# aka author
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

@login_required
def	event_detail(request, item_id):
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

@login_required
def	event_add(request):
	pass

@login_required
def	event_del(request, item_id):
	pass

@login_required
def	event_edit(request, item_id):
	pass

@login_required
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

@login_required
def	assign_accept(request, item_id):
	'''
	Accept action: set state to done
	'''
	item = Assign.objects.get(pk=item_id)
	item.read = True
	item.save()
	__log_it(request, item, CHANGE, u'Accepted')
	return HttpResponseRedirect(reverse('gw.views.assign_view', kwargs={'item_id': item.id}))

@login_required
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

@login_required
def	assign_approve(request, item_id):
	'''
	Approve action
	'''
	item = Assign.objects.get(pk=item_id)
	__log_it(request, item, CHANGE, u'Approved')
	return assign_accept(request, item_id)

@login_required
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

@login_required
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

@login_required
def	assign_history(request, item_id):
	return render_to_response('gw/task/assign_history.html', context_instance=RequestContext(request, {'item_list': LogEntry.objects.filter(object_id = item_id).order_by('action_time')}))
