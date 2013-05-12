# -*- coding: utf-8 -*-
'''
lansite.apps.task.views
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponse #, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

# 2. python
from datetime import datetime, date, time, timedelta
#import time

# 3. 3rd party
from icalendar import Calendar, Todo, UTC
import vobject
from objectpermissions.models import *	# http://sphinxdoc.github.com/django-object-permissions/

# 4. my
from models import *
from forms import *

# 5. siblings
from apps.core.forms import UserListForm

'''
TODO:
* 
todo_addsub:	Add sub todo
todo_onsub:	Make todo as child of
todo_unsub:	Get todo from children of
task_done (empty)
assign_invalid:	Invalid action: set state to done, w/ comments
assign_duped:	Duplicate action set state to done, w/ comments
assign_route: Route action: set assignee to new; set state to new;
assign_accept: set state to done
assign_done
assign_approve
assign_reopen
assign_mksub
assign_history
'''

datetype = type(date)
datetimetype = type(datetime)
PAGE_SIZE=20

@login_required
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
	user = User.objects.get(pk=request.user.id)	# aka author
	__handle_sortfilter(request, user, s_form)
	o_list = ToDoCat.objects.filter(author=user)
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		o_list = o_list.order_by(s)
	head = __mkdefpd((
		(u'Наименование', 'name'),
	), sort_o, sort_v)
	return render_to_response('task/todocat_list.html', context_instance=RequestContext(request, {
		'object_list': o_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Категории',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('apps.task.views.todocat_add'), 'type': 0},
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
			object = form.save(commit=False)
			object.author = User.objects.get(pk=request.user.id)
			object.save()
			return redirect('apps.task.views.todo_list')
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

@login_required
def	category_detail(request, object_id):
	return render_to_response('task/todocat_view.html', context_instance=RequestContext(request, {'object': ToDoCat.objects.get(pk=object_id)}))

@login_required
def	category_edit(request, object_id):
	object = ToDoCat.objects.get(pk=object_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST, instance=object)
		if form.is_valid():
			form.save()
			return redirect('apps.task.views.todo_list')
	else:	# GET
		form = ToDoCatForm(instance=object)
	return render_to_response('task/todocat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

@login_required
def	category_del(request, object_id):
	ToDoCat.objects.get(pk=object_id).delete()
	return redirect('apps.task.views.todo_list')

@login_required
def	category_add_todo(request, object_id):
	cat = ToDoCat.objects.get(pk=object_id)
	if request.method == 'POST':
		form = ToDoOfCatForm(request.POST)
		if form.is_valid():
			object = form.save(commit=False)
			object.author = User.objects.get(pk=request.user.id)
			object.category = cat
			object.save()
			return redirect('apps.task.views.todocat_view', object_id= cat.id)
	else:	# GET
		form = ToDoOfCatForm()
	return render_to_response('task/todo_edt.html', context_instance=RequestContext(request, {'form': form}))

@login_required
def	index(request):
	'''
	FIXME: handle settings and redirect to todo, contacts etc
	'''
	return render_to_response('task/index.html', context_instance=RequestContext(request))

@login_required
def	task_index_all(request):
	'''
	FIXME: handle settings and redirect to todo, contacts etc
	'''
	return redirect('apps.task.views.todo_index')
	s_form = 'task_list'
	user = User.objects.get(pk=request.user.id)
	__handle_sortfilter(request, user, s_form)
	o_list = Task.objects.all()
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		o_list = o_list.order_by(s)
	head = __mkdefpd((
		(u'Тип', 'type'),
		(u'Автор', 'user'),
		(u'Создано', 'created'),
		(u'Изменено', 'updated'),
		(u'Тема', 'summary'),
		(u'Состояние', 'status'),
		(u'Видимость', 'restriction'),
	), sort_o, sort_v)
	return render_to_response('task/task_list.html', context_instance=RequestContext(request, {
		'object_list': o_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задачи',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить Задание', 'url': reverse('apps.task.views.todo_add'), 'type': 0},
					{ 'name': 'Добавить Событие', 'url': reverse('apps.task.views.event_add'), 'type': 0},
					{ 'name': 'Убрать сортировку', 'url': '?a=s&v=0', 'type': 0},
					{ 'name': 'Убрать фильтры', 'url': '?a=f&v=*', 'type': 0},
					{ 'name': 'Удалить', 'url': '#', 'type': 0},
				),
			},
			'head':	head,
		},
	}))

@login_required
def	task_detail(request, object_id):
	# user_type = ContentType.objects.get_for_model(User)
	cid = Task.objects.get(pk=object_id).getclassid()
	if (cid == 1):
		v = 'apps.task.views.todo_detail'
	if (cid == 2):
		v = 'apps.task.views.assign_detail'
	return redirect(v, object_id=object_id)

@login_required
def	task_del(request, object_id):
	pass

@login_required
def	task_edit(request, object_id):
	pass

@login_required
def	ical_index(request):
	s_form = 'ical_list'
	user = User.objects.get(pk=request.user.id)	# aka author
	__handle_sortfilter(request, user, s_form)
	o_list = Assign.objects.filter(Q(author=user) | Q(assignee=user))
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)
	if s:
		o_list = o_list.order_by(s)
	for f in UserSetting.objects.filter(user=user, form=s_form, action='filter'):
		o = f.object
		v = int(f.value)
		if o == 'category':
			object_list = o_list.filter(category__id=v)
		if o == 'author':
			if (v == 0):
				o_list = o_list.exclude(author__id=v)
			else:
				o_list = o_list.filter(author__id=v)
		if o == 'assignee':
			if (v == -1):
				o_list = o_list.filter(assignee=None)
			elif (v == 0):
				o_list = o_list.exclude(assignee__id=v)
			else:
				o_list = o_list.filter(assignee__id=v)
		if o == 'done':
			o_list = o_list.filter(done=bool(v))
		if o == 'read':
			o_list = o_list.filter(read=bool(v))
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
	for i in User.objects.exclude(user=user):
		head[3]['menu'][2]['url'].append({'name': i.username, 'url': '?a=f&o=author&v=%d' % i.id})
	# filter on attendee
	head[4]['menu'].append(
		{ 'name': 'Show only', 'type': 1, 'url': (
			{'name': u'&lt;Все&gt;', 'url': '?a=f&o=assignee&v=*'},
			{'name': u'&lt;Мне&gt', 'url': '?a=f&o=assignee&v=%d' % user.id},
			{'name': u'&lt;Не мне&gt', 'url': '?a=f&o=assignee&v=0'},
			{'name': u'&lt;Никому&gt', 'url': '?a=f&o=assignee&v=-1'},
		)},
	)
	for i in User.objects.exclude(user=user):
		head[4]['menu'][2]['url'].append({'name': i.username, 'url': '?a=f&o=assignee&v=%d' % i.id})
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
	return render_to_response('task/assign_list.html', context_instance=RequestContext(request, {
		'object_list': o_list,
		'data': {
			'title': {
				'id':		'main',
				'name':		'Задания',
				'title':	'',
				'menu':		(
					{ 'name': 'Добавить', 'url': reverse('apps.task.views.assign_add'), 'type': 0},
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
	user = User.objects.get(pk=request.user.id)	# aka author
	# 1. get and save params (of URL - into settings)
	__handle_sortfilter(request, user, s_form)
	# 2. prepare data
	o_list = vToDo.objects.all()
	# my or for me or public
	o_list = o_list.filter(user=user) | o_list.filter(attendee=user) | o_list.filter(restriction=1)
	sort_o, sort_v, s = UserSetting.objects.get_sort(user=user, form=s_form)	# ..., s: sort order
	# ... columns to show
	columns_form = ColumnsForm()
	hcol_dict = dict()
	for c in UserSetting.objects.filter(user=user, form=s_form, action='column', value='0'):
		hcol_dict[c.object] = True
		columns_form.fields[c.object].initial = False
	object_head = list()
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
			object_head.append(k)
	# 3. sort
	sort_form = SortForm()
	if s:
		if s.startswith('-'):
			sort_form.fields[s[1:]].initial = 1
		else:
			sort_form.fields[s].initial = 2
		o_list = o_list.order_by(s)
	# 4. filter (user, status, restriction; attendee, priority)
	filter_form = FilterForm()
	#for u in User.objects.all():
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
			o_list = o_list.filter(user=int(v))
			filter_form.fields[o].initial = User.objects.get(pk=int(v))
		if o == 'status':
			o_list = o_list.filter(status=int(v))
		if o == 'restriction':
			o_list = o_list.filter(restriction=int(v))
		if o == 'attendee':
			o_list = o_list.filter(attendee__id=int(v))
			filter_form.fields[o].initial = User.objects.get(pk=int(v))
		if o == 'priority':
			if v == '0':
				o_list = o_list.filter(priority=None)
			else:
				o_list = o_list.filter(priority=int(v))
		if o == 'categories':
			o_list = o_list.filter(categories=int(v))
			current_cat = int(v)
	# 5. prepare menus
	# x. let's go
	cat_list = __getneedcats(user, ContentType.objects.get_for_model(vToDo))
	return object_list (
		request,
		queryset = o_list,
		template_name = 'task/todo_list.html',
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		extra_context = {
			'cat_list': cat_list,		# Query of my categories
			'current_cat': current_cat,	# int - id of selected category
			'hcol_dict': hcol_dict,
			'object_head': object_head,
			'columns_form': columns_form,
			'sort_form': sort_form,
			'filter_form': filter_form,
			#'t0': time.time()
		}
	)

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
	return redirect('apps.task.views.todo_index')

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
	return redirect('apps.task.views.todo_index')

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
	return redirect('apps.task.views.todo_index')

@login_required
def	todo_add(request):
	form = ToDoForm(request.POST or None)
	if form.is_valid():
		object = form.save(commit=False)
		object.user = User.objects.get(pk=request.user.id)
		object.created = datetime.now()
		object.updated = datetime.now()
		object.save()
		form.save_m2m()
		return redirect('apps.task.views.todo_index')
	return direct_to_template(request, 'task/todo_form.html', {'form': form})

@login_required
def	todo_detail(request, object_id):
	'''
	TODO:
		* master_form: exclude self & above & below todos
		* get all available perms (or const 'cause I know available perms)
		* get all users of this object
		* test permissions of each user
	'''
	object = vToDo.objects.get(pk=object_id)
	#xq = object.taskcat_set.all().values_list('cat__id', flat=True)
	#q = __getneedcats(user = User.objects.get(pk=request.user.id), app = ContentType.objects.get_for_model(vToDo)).exclude(id__in=xq)
	#if (q):
	#	form = ChoiceForm(q = q)
	#else:
	#	form = None
	user = User.objects.get(pk=request.user.id)
	cols = UserSetting.objects.filter(user=user, form='todo_detail', action='cols')
	cols = int(cols[0].value) if cols else 1
	return object_detail (
		request,
		queryset = vToDo.objects.all(),
		object_id = object_id,
		template_name = 'task/todo_detail.html',
		extra_context = {
			'table': {
				1: 'task/todo_detail1.html',
				2: 'task/todo_detail2.html',
				3: 'task/todo_detail3.html',
			}[cols]
		}
	)

@login_required
def	todo_detail_setcols(request, object_id, cols):
	'''
	Set detail/edit templates to 1/2/3 columns
	'''
	user = User.objects.get(pk=request.user.id)
	UserSetting.objects.filter(user=user, form='todo_detail', action='cols').delete()
	UserSetting.objects.create(user=user, form='todo_detail', action='cols', object='cols', value=cols)
	#return redirect('apps.task.views.todo_detail', object_id = object_id)
	return redirect(vToDo.objects.get(pk=object_id).get_absolute_url())

@login_required
def	todo_links(request, object_id):
	object = vToDo.objects.get(pk=object_id)
	x = list()
	# a. exclude self
	x.append(object.id)
	# b. exclude parents
	x.extend(object.lefts.all().values_list('left', flat = True))
	# c. exclude children
	x.extend(object.rights.all().values_list('right', flat = True))
	return object_detail (
		request,
		queryset = vToDo.objects.all(),
		object_id = object_id,
		template_name = 'task/todo_links.html',
		extra_context = {
			'master_form': ChoiceForm(vToDo.objects.exclude(pk__in=x)),
		}
	)

@login_required
def	todo_perm_view(request, object_id):
	'''
	View object permissions
	'''
	object = vToDo.objects.get(pk=object_id)
	# d. permissions
	# d.1. Head (all available permissions as string list
	perm_head = list()
	for i in object.perms:
		perm_head.append(i)	# str; or object.perms[i] - int
	# d.2. Details.Groups
	perm_list_group = list()		# list of all users and their permissions as bit mask
	for p in GroupPermission.objects.filter(vtodo = object):	# cool!
		a = { 'u': p.group, 'p': list() }
		for i in perm_head:
			a['p'].append(p.group.has_object_perm(object, i))
		perm_list_group.append(a)
	# d.3. Details.Users
	perm_list_user = list()		# list of all users and their permissions as bit mask
	for p in UserPermission.objects.filter(vtodo = object):	# cool!
		perm_list = UserPermission.bits(p.permission)
		perm_list.reverse()
		perm_list_user.append({ 'u': p.user, 'p': perm_list })
	return render_to_response('task/todo_perms.html', context_instance=RequestContext(request, {
		'object': object,
		'perm_head': perm_head,
		'perm_list_group': perm_list_group,
		'form_group': ChoiceForm(Group.objects.all()),	# FIXME: unused groups only
		'perm_list_user': perm_list_user,
		'form_user': ChoiceForm(User.objects.all()),	# FIXME: unused users only
	}))

@login_required
def	todo_perm_setg(request, object_id):
	'''
	Set group permissions on object
	'''
	object = vToDo.objects.get(pk=object_id)
	return redirect('apps.task.views.todo_perm_view', object_id = object_id)

@login_required
def	todo_perm_delg(request, object_id):
	'''
	Del group permissions of object
	'''
	object = vToDo.objects.get(pk=object_id)
	return redirect('apps.task.views.todo_perm_view', object_id = object_id)

@login_required
def	todo_perm_setu(request, object_id):
	'''
	Set group permissions on object
	'''
	object = vToDo.objects.get(pk=object_id)
	form = ChoiceForm(User.objects.all(), request.POST)
	if form.is_valid():
		user = form.cleaned_data['object']
		for i in set(map(int, request.POST.getlist('perm'))):
			user.grant_object_perm(object, permissions[i])
	return redirect('apps.task.views.todo_perm_view', object_id = object_id)

@login_required
def	todo_perm_delu(request, object_id):
	'''
	Del user permissions of object
	'''
	object = vToDo.objects.get(pk=object_id)
	userlist = set(map(int, request.POST.getlist('user')))
	UserPermission.objects.filter(user__pk__in = userlist, vtodo = object).delete()
	return redirect('apps.task.views.todo_perm_view', object_id = object_id)

@login_required
def	todo_log(request, object_id):
	object = vToDo.objects.get(pk=object_id)
	return render_to_response('task/todo_log.html', context_instance=RequestContext(request, {'object': object}))

@login_required
def	todo_tags(request, object_id):
	object = vToDo.objects.get(pk=object_id)
	return render_to_response('task/todo_tags.html', context_instance=RequestContext(request, {'object': object}))

@login_required
def	todo_edit(request, object_id):
	object = vToDo.objects.get(pk=object_id)
	form = ToDoForm(request.POST or None, instance=object)
	if form.is_valid():
		object = form.save(commit=False)
		object.updated = datetime.now()
		object = form.save()
		return redirect(object.get_absolute_url())
	return direct_to_template(request, 'task/todo_form.html', {'object': object, 'form': form})

@login_required
def	todo_del(request, object_id):
	vToDo.objects.get(pk=object_id).delete()
	return redirect('apps.task.views.todo_index')	# FIXME: next

@login_required
def	todo_done(request, object_id):
	object = ToDo.objects.get(pk=object_id)
	object.done = True
	object.save()
	return redirect('apps.task.views.todo_list')

@login_required
def	todo_cat_add(request):
	'''
	Add new Category for ToDo list
	'''
	form = CategoryForm(request.POST or None)
	if form.is_valid():
		object = form.save(commit=False)
		if (form.cleaned_data['thisuser']):
			object.user = User.objects.get(pk=request.user.id)
		else:
			object.user = None
		if (form.cleaned_data['thisapp']):
			object.app = ContentType.objects.get_for_model(vToDo)
		else:
			object.app = None
		object = form.save()
		return redirect('apps.task.views.todo_index')
	return direct_to_template(request, 'task/todo_cat_edit.html', {'form': form})

@login_required
def	todo_cat_edit(request, object_id):
	'''
	Edit category in ToDo list
	'''
	object = Category.objects.get(pk=object_id)
	user = User.objects.get(pk=request.user.id)
	app = ContentType.objects.get_for_model(vToDo)
	#print object.user == request.user, object.app == ContentType.objects.get_for_model(vToDo)
	#print object.user == user, object.app, ContentType.objects.get_for_model(vToDo)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance = object, initial = {'thisuser': object.user == user, 'thisapp': object.app == app})
		if form.is_valid():
			object = form.save(commit=False)
			if (form.cleaned_data['thisuser']):
				object.user = user
			else:
				object.user = None
			if (form.cleaned_data['thisapp']):
				object.app = app
			else:
				object.app = None
			object = form.save()
			return redirect('apps.task.views.todo_index')
	else:
		form = CategoryForm(instance = object, initial = {'thisuser': object.user == user, 'thisapp': object.app == app})
	return direct_to_template(request, 'task/todo_cat_edit.html', {'form': form})

@login_required
def	todo_addcat(request, object_id):
	'''
	Add category to todo (in detail mode ?..)
	'''
	object = vToDo.objects.get(pk=object_id)
	form = ChoiceForm(Category.objects.all(), request.POST)
	if form.is_valid():
		TaskCat(task=object, cat=form.cleaned_data['object']).save()
	return redirect('apps.task.views.todo_detail', object_id=int(object_id))

@login_required
def	todo_delcat(request, object_id):
	'''
	object_id - TaskCat
	'''
	tc = TaskCat.objects.get(pk=object_id)
	todo = tc.task
	tc.delete()
	return redirect('apps.task.views.todo_detail', object_id = todo.id)

@login_required
def	todo_cat_del(request, object_id):
	'''
	object_id - Category
	'''
	Category.objects.get(pk=object_id).delete()
	return redirect('apps.task.views.todo_index')

@login_required
def	todo_cat_del_selected(request):
	for i in set(map(int, request.POST.getlist('cat'))):
		Category.objects.get(pk=i).delete()
	return redirect('apps.task.views.todo_index')

@login_required
def	todo_del_selected(request):
	for i in set(map(int, request.POST.getlist('todo'))):
		vToDo.objects.get(pk=i).delete()
	return redirect('apps.task.views.todo_index')

@login_required
def	todo_sub_add(request, object_id):
	'''
	Add sub-vToDo
	'''
	form = ChoiceForm(vToDo.objects.all(), request.POST)
	if form.is_valid():
		ObjectLink(left = vToDo.objects.get(pk = object_id), right = form.cleaned_data['object']).save()
	return redirect('apps.task.views.todo_links', object_id = object_id)

@login_required
def	todo_sub_del(request, object_id):
	'''
	Delete sub-vToDo
	'''
	object = ObjectLink.objects.get(pk=object_id)
	object_id = object.left.id
	object.delete()
	return redirect('apps.task.views.todo_detail', object_id = object_id)
@login_required
def	todo_ical_export(request):
	'''
	Type: iCalendar
	Mime: text/calendar
	Ext: ics
	#tpl = loader.get_template('task/todo.ics')
	#response.write(tpl.render(Context({'object_list': object_list})).encode('utf-8'))
	'''
	user = User.objects.get(pk=request.user.id)	# aka author
	response = HttpResponse(mimetype='text/calendar')
	response['Content-Disposition'] = '; filename=todo.ics'
	cal = Calendar()
	cal.add('version', '2.0')
	cal.add('prodid', '-//LanSite GroupWare//eap.su//')
	for object in vToDo.objects.filter(user=user):
		todo = Todo()
		# 1. Task
		#todo['created'] = object.created
		todo.add('created', object.created)
		todo.add('last-modified', object.updated)
		todo.add('summary', object.summary)
		if (object.getstatusname()):
			todo.add('status', object.getstatusname())
		if (object.getrestrictionname()):
			todo.add('class', object.getrestrictionname())
		if (object.getcategories()):
			todo.add('categories', object.getcategories())
		# 2. vCal
		if object.attendee:
			email = object.attendee.email
			if email:
				todo.add('attendee', 'MAILTO:%s' % email)
			email = user.email
			if email:
				todo.add('organizer', 'MAILTO:%s' % email)
		if object.description:
			todo.add('description', object.description)
		if object.start_d:
			if object.start_t:
				todo.add('dtstart', datetime.combine(object.start_d, object.start_t))
			else:
				todo.add('dtstart', object.start_d)
		if object.duration_d:
			if object.duration_t:
				todo.add('duration', timedelta(
					days=object.duration_d,
					hours=object.duration_t.hour,
					minutes=object.duration_t.minute,
					seconds=object.duration_t.second
				))
			else:
				todo.add('duration', timedelta(days=object.duration_d))
		if object.location:
			todo.add('location', object.location)
		if object.priority:
			todo.add('priority', object.priority)
		if object.URL:
			todo.add('URL', object.URL)
		# 3. vToDo
		if object.due_d:
			if object.due_t:
				todo.add('due', datetime.combine(object.due_d, object.due_t))
			else:
				todo.add('due', object.due_d)
		if object.completed:
			todo.add('completed', object.completed)
		if object.percent:
			todo.add('percent-complete', object.percent)
		cal.add_component(todo)
	response.write(cal.as_string())		# .encode('utf-8')
	return response

@login_required
def	__rawdt(dt):
	'''
	@param dt:?
	@return datetime object from dt
	'''
	return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

@login_required
def	todo_ical_import(request):
	result = list()
	if (request.method == 'POST'):
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			user = User.objects.get(pk=request.user.id)
			app = ContentType.objects.get_for_model(vToDo)
			mycats = __getneedcats(user, app)
			cal = Calendar.from_string(file.read())
			for cmp in cal.walk():
				cname = cmp.name
				if (cname == 'VTODO'):
					# TODO: attendee:MAILTO:user...@
					# 1. Task
					object = vToDo(user=user)
					object.created = __rawdt(cmp.decoded('created'))
					object.updated = __rawdt(cmp.decoded('last-modified'))
					object.summary = cmp.decoded('summary')
					object.status = VTODO_STATUS_REVERSE.get(cmp.decoded('status').upper(), None)
					object.restriction = RESTRICTION_REVERSE.get(cmp.decoded('class').upper(), None)
					# 2. vCal
					#object.attendee = cmp.decoded('attendee')
					attendee = cmp.decoded('attendee', None)
					if (attendee):
						users = User.objects.filter(user__email=attendee).order_by('user__username')
						if users.count():
							object.attendee = users[0]
					object.description = cmp.decoded('description', None)
					start = cmp.decoded('dtstart', None)
					if (start):
						if type(start) == datetype:
							object.start_d = start.date
							object.start_t = start.time
						else:
							object.start_d = start
					duration = cmp.decoded('duration', None)
					if (duration):
						if (duration.days):
							object.duration_d = duration.days
						if (duration.seconds):
							object.duration_t = (datetime.min + timedelta(0, duration.seconds)).time()
					object.location = cmp.decoded('location', None)
					object.priority = cmp.decoded('priority', None)
					object.URL = cmp.decoded('URL', None)
					# 3. vToDo
					due = cmp.decoded('due', None)
					if (due):
						if type(due) == datetype:
							object.due_d = due.date
							object.due_t = due.time
						else:
							object.due_d = due
					object.completed = cmp.decoded('completed', None)
					object.percent = cmp.decoded('percent-complete', None)
					# x. That's all
					object.save()
					# y. No, not all...
					cats = cmp.decoded('categories', None)
					if cats:
						for c in cats.split(','):
							findcat = mycats.filter(name=c).order_by('user', 'app')	# FIXME: 1. user+app, 2. app, 3. user
							if (findcat.count()):
								TaskCat(task=object, cat=findcat[0]).save()
							else:
								cat = Category(name=c, user=user, app=app)
								cat.save()
								TaskCat(task=object, cat=cat).save()
			return redirect('apps.task.views.todo_index')
	else:
		form = FileUploadForm()
	return render_to_response('task/todo_ical_upload.html', context_instance=RequestContext(request, {'form': form, 'result': result}))

@login_required
def	todo_ical_export2(request):
	user = User.objects.get(pk=request.user.id)	# aka author
	response = HttpResponse(mimetype='text/calendar')
	response['Content-Disposition'] = '; filename=todo_2.ics'
	cal = vobject.iCalendar()
	for object in vToDo.objects.filter(user=user):
		todo = cal.add('vtodo')
		# 1. Task
		todo.add('created').value = object.created
		todo.add('last-modified').value = object.updated
		todo.add('summary').value = object.summary
		if (object.getstatusname()):
			todo.add('status').value = object.getstatusname()
		if (object.getrestrictionname()):
			todo.add('class').value = object.getrestrictionname()
		if (object.categories):
			todo.add('categories').value = object.taskcat_set.all().values_list('cat__name', flat=True)
		# 2. vCal
		if object.attendee:
			email = object.attendee.email
			if email:
				todo.add('attendee').value = 'MAILTO:%s' % email
			email = user.email
			if email:
				todo.add('organizer').value = 'MAILTO:%s' % email
		if object.description:
			todo.add('description').value = object.description
		if object.start_d:
			if object.start_t:
				todo.add('dtstart').value = datetime.combine(object.start_d, object.start_t)
			else:
				todo.add('dtstart').value = object.start_d
		if object.duration_d:
			if object.duration_t:
				todo.add('duration').value = timedelta(
					days=object.duration_d,
					hours=object.duration_t.hour,
					minutes=object.duration_t.minute,
					seconds=object.duration_t.second
				)
			else:
				todo.add('duration').value = timedelta(days=object.duration_d)
		if object.location:
			todo.add('location').value = object.location
		if object.priority:
			todo.add('priority').value = str(object.priority)	# hack
		if object.URL:
			todo.add('URL').value = object.URL
		# 3. vToDo
		if object.due_d:
			if object.due_t:
				todo.add('due').value = datetime.combine(object.due_d, object.due_t)
			else:
				todo.add('due').value = object.due_d
		if object.completed:
			todo.add('completed').value = object.completed
		if object.percent:
			todo.add('percent-complete').value = object.percent
	#cal.prettyPrint()
	response.write(cal.serialize())		# .encode('utf-8')
	return response

@login_required
def	todo_ical_import2(request):
	result = list()
	if (request.method == 'POST'):
		form = FileUploadForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			user = User.objects.get(pk=request.user.id)
			app = ContentType.objects.get_for_model(vToDo)
			mycats = __getneedcats(user, app)
			cal = vobject.readOne(file.read())
			for cmp in cal.vtodo_list:
				#cname = cmp.name
				#if (cname == 'VTODO'):
				# TODO: attendee:MAILTO:user...@
				# 1. Task
				#print cmp.contents.knownChildren
				object = vToDo(user=user)
				categories = list()
				for parm in cmp.contents:
					name = cmp.contents[parm][0].name
					value = cmp.contents[parm][0].value
					# 1. Task
					if (name == 'CREATED'):
						object.created = value
					elif (name == 'LAST-MODIFIED'):
						object.updated = value
					elif (name == 'SUMMARY'):
						object.summary = value
					elif (name == 'STATUS'):
						object.status = VTODO_STATUS_REVERSE.get(value.upper(), None)
					elif (name == 'CLASS'):
						object.status = RESTRICTION_REVERSE.get(value.upper(), None)
					# vCal
					elif (name == 'ATTENDEE'):
						users = User.objects.filter(email=value).order_by('username')
						if users.count():
							object.attendee = users[0]
					elif (name == 'DESCRIPTION'):
						object.description = value
					elif (name == 'DTSTART'):
						if type(value) == datetype:
							object.start_d = value.date
							object.start_t = value.time
						else:
							object.start_d = value
					elif (name == 'DURATION'):
						if (value.days):
							object.duration_d = value.days
						if (value.seconds):
							object.duration_t = (datetime.min + timedelta(0, value.seconds)).time()
					elif (name == 'LOCATION'):
						object.location = value
					elif (name == 'PRIORITY'):
						object.priority = value
					elif (name == 'URL'):
						object.URL = value
					# 3. vToDo
					elif (name == 'DUE'):
						if type(value) == datetype:
							object.due_d = value.date
							object.due_t = value.time
						else:
							object.due_d = value
					elif (name == 'COMPLETED'):
						object.completed = value
					elif (name == 'PERCENT-COMPLETE'):
						object.percent = value
					elif (name == 'CATEGORIES'):
						categories = value[:]
					# 4. else
					elif (name == 'ORGANIZER'):
						pass
					elif (name == 'UID'):
						pass
					else:
						print 'Unknown key', name, ':', value
				object.save()
				for c in categories:
					findcat = mycats.filter(name=c).order_by('user', 'app')	# FIXME: 1. user+app, 2. app, 3. user
					if (findcat.count()):
						TaskCat(task=object, cat=findcat[0]).save()
					else:
						cat = Category(name=c, user=user, app=app)
						cat.save()
						TaskCat(task=object, cat=cat).save()
			return redirect('apps.task.views.todo_index')
	else:
		form = FileUploadForm()
	return render_to_response('task/todo_ical_upload2.html', context_instance=RequestContext(request, {'form': form, 'result': result}))
'''
http://blog.thescoop.org/archives/2007/07/31/django-ical-and-vobject/

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    for event in event_list:
        vevent = cal.add('vevent')
        ... # add your event details
    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=filename.ics
'''