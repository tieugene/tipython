# -*- coding: utf-8 -*-

'''
lansite.apps.core.models
FIXME: gw | course, gw | skill, gw | gwuser, gw | speciality, gw | personskill
TODO: Logged
	* m2m
	* FK, OneToOne
	* check endpoint class (don't log parent object)
	* old_pk and old_pk != new_pk
NOTE:
	* Json exports self fields only - not inherited
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

# 2. 3rd party
from polymorphic import PolymorphicModel
from treebeard.al_tree import AL_Node

# 3. my
from settings import LOGIN_REDIRECT_URL, LOGGER

from apps.ref.models import Kladr
from apps.mid import get_request

class	LogEntryField(models.Model):
	logentry	= models.ForeignKey(LogEntry, verbose_name=u'Запись журнала')
	field		= models.CharField(max_length=255, verbose_name=u'Поле')
	value		= models.CharField(max_length=255, verbose_name=u'Значение')

	def __unicode__(self):
		return u'%s: %s' % (self.field, self.value)

	class    Meta:
		app_label		= 'gw'
		unique_together		= (('logentry', 'field',),)
		ordering		= ('id',)
		verbose_name		= u'Изменение полей'

def	_2dict(object):
	'''
	return dict of fieldname:fieldvalue (in native format)
	FIXME: http://www.djangofoo.com/tag/meta-fields
	'''
	retvalue = dict()
	for field in object._meta.fields:
		retvalue[field.name] = getattr(object, field.name)
	return retvalue

def	_log_it(request, object, flag, fields = None):
	'''
	Save log for object
	'''
	if (flag == DELETION) or fields:
		le = LogEntry.objects.create (
			user		= request.user,
			content_type	= ContentType.objects.get_for_model(object),
			object_id	= object.pk,
			object_repr	= str(object)[:200],
			action_flag	= flag,	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
			change_message	= u'UI',
		)
		for fn, fv in fields.iteritems():
			LogEntryField.objects.create(
				logentry = le,
				field = fn,
				value = fv,
			)

class	Logged(object):
	'''
	Abstract class for logging object changes
	'''
	def    raw_save(self, force_insert = False, force_update = False, using=''):
		'''
		For import only
		'''
		if issubclass(self.__class__, PolymorphicModel):
			PolymorphicModel.save(self, force_insert = force_insert, force_update = force_update)
		else:
			models.Model.save(self, force_insert = force_insert, force_update = force_update, using = using)

	def	save(self, force_insert = False, force_update = False, using=''):
		'''
		'''
		# 1. get old values
		old_pk = self.pk
		old_attrs = dict()
		#try:
		if old_pk:
			old_attrs = _2dict(self.__class__.objects.get(pk = old_pk))
		#except:
		#	old_attrs = dict()
		# 2. save object
		if issubclass(self.__class__, PolymorphicModel):
			PolymorphicModel.save(self, force_insert = force_insert, force_update = force_update)
		else:
			models.Model.save(self, force_insert = force_insert, force_update = force_update, using = using)
		# 3. get new values
		new_pk = self.pk
		new_attrs = dict()
		if new_pk:
			new_attrs = _2dict(self)
		# 4. compare and log
		if new_pk:		# everything ok
			if old_pk:	# update
				for k, v in old_attrs.iteritems():
					if k in new_attrs and v == new_attrs[k]:
						del new_attrs[k]
				_log_it(get_request(), self, CHANGE, new_attrs)
			else:		# create
				_log_it(get_request(), self, ADDITION, new_attrs)

	def delete(self):
		_log_it(get_request(), self, DELETION)
		models.Model.delete(self)

class	USManager(models.Manager):
	'''
	UserSetting manager
	'''
	def	cu_ufa(self, user, form, action, object, value):
		'''
		Create or update object/value/ for given user/form/action
		Used for sort set
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		@param o:str - string
		@param v:str - string
		'''
		q = self.filter(user=user, form=form, action=action)
		if (q):
			r = q[0]
			if ((r.object != object) or (r.value != value)):
				r.object = object
				r.value = value
				r.save()
		else:
			UserSetting(user=user, form=form, action=action, object=object, value=value).save()

	def	cu_ufao(self, user, form, action, object, value):
		'''
		Create or update object/value/action/ for given user/form/action/object
		Used for filter set
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		@param o:str - string
		@param v:str - string
		'''
		q = self.filter(user=user, form=form, action=action, object=object)
		if (q):
			r = q[0]
			if (r.value != value):
				r.value = value
				r.save()
		else:
			UserSetting(user=user, form=form, action=action, object=object, value=value).save()

	def	del_ufao(self, user, form, action, object = None):
		'''
		Delete all of given user/form/actions
		Used for delete sort|filters
		@param self:UserSetting object
		@param u:str - string
		@param f:str - string
		@param a:str - string
		'''
		if (o is None):
			self.filter(user=user, form=form, action=action).delete()
		else:
			self.filter(user=user, form=form, action=action, object=object).delete()

	def	get_sort(self, user, form):
		'''
		@return (order:str, name:str, value:int)
		'''
		retvalue = (None, None, None)
		sort = self.filter(user=user, form=form, action='sort')
		if sort:
			o = sort[0].object
			v = int(sort[0].value)	# 1/-1
			print sort[0].value
			if (v == 1):
				retvalue = (o, v, '-' + o)
			else:
				retvalue = (o, v, o)
		return retvalue

class	UserSetting(models.Model):
	user		= models.ForeignKey(User, blank=False, null=False, verbose_name=u'Пользователь')
	form		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Форма')
	action		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Действие')
	object		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Объект')
	value		= models.CharField(max_length=16, blank=False, null=False, verbose_name=u'Значение')
	objects		= USManager()

	def	__unicode__(self):
		return u'%s.%s.%s.%s.%s' % (self.user.username, self.form, self.object, self.action, self.value )

	class	Meta:
		app_label = 'gw'
		ordering = ('user', 'form', 'object', 'action')
		verbose_name = u'Настройки пользователя'
		verbose_name_plural = u'Настройки пользователей'

class	Object(PolymorphicModel):
	'''
	General lansite parent.
	TODO: links => children, w/o model; links: symmetric
	'''
	links	= models.ManyToManyField('self', symmetrical=False, through='ObjectLink', verbose_name=u'Объекты')

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'Объект'
		verbose_name_plural	= u'Объекты'

class	ObjectLink(models.Model):
	'''
	master		= models.ForeignKey(Object, related_name='slave', verbose_name=u'Хозяин')
	slave		= models.OneToOneField(Object, related_name='master', primary_key=True, verbose_name=u'Объект')
	TODO: left => master; right => slave
	'''
	left		= models.ForeignKey(Object, related_name='rights', verbose_name=u'Слева')
	right		= models.ForeignKey(Object, related_name='lefts', verbose_name=u'Справа')

	class	Meta:
		app_label = 'gw'
		unique_together		= (('left', 'right',),)
		verbose_name		= u'Связь'
		verbose_name_plural	= u'Связи'
"""
FIXME: cant delete inherited from Object
class	RDF(models.Model):
	subject		= models.ForeignKey(Object, related_name='objects', verbose_name=u'Субъект')
	object		= models.ForeignKey(Object, related_name='subjects', verbose_name=u'Объект')
	link		= models.ForeignKey(Object, null=True, related_name='pairs', verbose_name=u'Связь')

	class	Meta:
		app_label = 'gw'
		unique_together		= (('subject', 'object',),)
		verbose_name		= u'RDF'
		verbose_name_plural	= u'RDFs'
"""
"""
class	ObjectSq(Object):
	'''
	Object sequence.
	Methods: push, pop, swap[, insert, delete]
	'''
	'''
	child	= models.ManyToManyField('self', symmetrical=False, through='SubObject', verbose_name=u'Объекты')
	'''

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'Последовательность объектов'
		verbose_name_plural	= u'Последовательности объектов'
"""
"""
class    Permissions(models.Model):
		'''
		Readme:
			= GenPerm =
			http://www.djangoproject.com/documentation/models/generic_relations/
			http://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
			= Std permissions extending =
			http://www.satchmoproject.com/blog/2008/nov/28/using-django-permissions/
			= Per-object =
			http://bitbucket.org/jezdez/django-authority/
			http://code.google.com/p/django-granular-permissions/
			https://bitbucket.org/diefenbach/django-permissions
			https://github.com/washingtontimes/django-objectpermissions
			http://djangoadvent.com/1.2/object-permissions/
			
		perm = enum(Create?, Read, Update, Delete, SetPermissions) (Note: Create can't be for object)
		if object_id == 0 then permissions - for model
		TODO: try register Read in Django permissions
		'''
		content_type	= models.ForeignKey(ContentType, null=False, blank=False, verbose_name=u'Модель')
		object_id	= PositiveIntegerField(null=False, blank=False, verbose_name=u'Объект')
		user		= models.ForeignKey(User, null=False, blank=False, verbose_name=u'Пользователь')
		perm		= PositiveSmallIntegerField(null=False, blank=False, default=0, verbose_name=u'Права')
		ban		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Запрет')

		def    asstr(self):
			return u'%s.%s' % (self.model, self.object)

		def    __unicode__(self):
			return self.asstr()

		class    Meta:
		app_label = 'gw'
		ordering = ('content_type','object_id')
		verbose_name = u'Право'
		verbose_name_plural = u'Права'
		unique_together = [('content_type', 'object_id', 'user')]
"""
class	AddrShort(models.Model):
	'''
	Сокращение для адреса: ул.=улица etc
	'''
	name		= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Полное наименование')

	def	__unicode__(self):
		return u'%s (%s)' % (self.name, self.fullname)

	class	Meta:
		app_label = 'gw'
		ordering		= ('name', )
		verbose_name		= u'Сокращение адреса'
		verbose_name_plural	= u'Сокращения адресов'

class	AddrType(models.Model):
	'''
	Тип адреса: Домашний, Юридический, Почтовый, Доставки etc
	RFC2426:
	dom	- domestic delivery address - местный (в местном формате)
	intl	- international delivery address - международный
	postal	- postal delivery address - почтовый
	parcel	- parcel delivery address - доставки
	home	- a delivery address for a residence - домашний
	work	- delivery address for a place of work - рабочий (места работы)
	pref	- preferred delivery address when more than one address is specified - основной
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	abbr		= models.CharField(max_length=6, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	name		= models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип адреса'
		verbose_name_plural	= u'Типы адресов'

class	Address(Object, AL_Node):
	'''
	Адрес (РФ) - рекурсивный
	'''
	name		= models.CharField(max_length=60, null=False, blank=False, verbose_name=u'Наименование')
	type		= models.ForeignKey(AddrShort, null=True, blank=True, verbose_name=u'Сокращение')
	typeplace	= models.SmallIntegerField(null=True, blank=True, verbose_name=u'Расположение сокращения')	# type пишется слева, справа, в середине
	parent		= models.ForeignKey('self', related_name='children_set', null=True, db_index=True, verbose_name=u'Предок')
	publish		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Печатать')
	endpoint	= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Конец')
	zip		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Индекс')
	fullname	= models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Полный адрес')
	node_order_by	= ['name']

	def	__unicode__(self):
		return self.name

	def	asfullstr(self):
		retvalue = u''
		for i in self.getparents():
			retvalue = retvalue + i.name + ', '
		return retvalue + self.name

	def	mkfullname(self, country):
		'''
		Build full name recursively
		'''
		if self.endpoint:
			tmp = list()
			for i in self.get_ancestors():
				if i.publish:
					if i.type:
						tmp.append(i.type.name + u'. ' + i.name)
					else:
						if country:
							tmp.append(i.name)
						elif i.parent != None:
							tmp.append(i.name)	 
			if self.publish:
				if self.type:
					tmp.append(self.type.name + u'. ' + self.name)
				else:
					tmp.append(self.name)
			self.fullname = ', '.join(tmp)
		else:
			self.fullname = self.name
			
	def getfullname(self):
		self.mkfullname(False)
		return self.fullname
			
	def __getfullname_country(self):
		self.mkfullname(True)
		return (str(self.zip) + ', ' + self.fullname)
	
	getfullname_country = property(__getfullname_country)
		
	@models.permalink
	def	get_absolute_url(self):
		return ('apps.core.views.address_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.core.views.address_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.core.views.address_del', [str(self.pk)])

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'Адрес'
		verbose_name_plural	= u'Адреса'
		ordering		= ('name',)

class	AddrKladr(models.Model):
	address		= models.OneToOneField(Address, verbose_name=u'Адрес')
	kladr		= models.ForeignKey(Kladr, null=False, blank=False, db_index=True, verbose_name=u'КЛАДР')

	def	__unicode__(self):
		return self.address

	class	Meta:
		app_label = 'gw'
		verbose_name		= u'Адрес.Кладр'
		verbose_name_plural	= u'Адреса.Кладр'

class	PhoneType(models.Model):
	'''
	Тип телефона
	RFC2426:
	home	- a telephone number associated with a residence
	msg	- the telephone number has voice messaging support
	work	- telephone number associated with a place of work
	pref	- a preferred-use telephone number
	voice	- voice telephone number (default)
	fax	- facsimile telephone number
	cell	- cellular telephone number
	video	- a video conferencing telephone number
	pager	- paging device telephone number
	bbs	- bulletin board system telephone number
	modem	- a MODEM connected telephone number
	car	- a car-phone telephone number
	isdn	- an ISDN service telephone number
	pcs	- personal communication services telephone number
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	abbr		= models.CharField(max_length=5, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	name		= models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		app_label = 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип телефона'
		verbose_name_plural	= u'Типы телефонов'

class	Phone(Object):
	'''
	Телефонный номер.
	'''
	no		= models.CharField(max_length=15, null=False, blank=False, unique=True, verbose_name=u'Номер')
	types		= models.ManyToManyField(PhoneType, through='Phone2Type', verbose_name=u'Типы')

	def	__unicode__(self):
		return self.no

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.core.views.phone_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.core.views.phone_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.core.views.phone_del', [str(self.pk)])

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'Телефон'
		verbose_name_plural	= u'Телефоны'
		ordering		= ('no',)

class	Phone2Type(models.Model):
	type		= models.ForeignKey(PhoneType, null=False, blank=False, verbose_name=u'Тип')
	phone		= models.ForeignKey(Phone, null=False, blank=False, verbose_name=u'Телефон')

	def	__unicode__(self):
		return u'%s: %s' % (self.phone, self.type)

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'Телефон.Тип'
		verbose_name_plural	= u'Телефон.Типы'
		ordering		= ('phone', 'type',)
		unique_together		= (('type', 'phone',),)
"""
class	__URL(Object):
	URL		= models.URLField(unique=True, verbose_name=u'URL')

	def	__unicode__(self):
		return self.URL

	class	Meta:
		app_label		= 'gw'
		ordering		= ('URL',)
		abstract		= True
"""
class	WWW(Object):
	'''
	Web-ресурс.
	'''
	URL		= models.URLField(unique=True, verbose_name=u'URL')

	def	__unicode__(self):
		return self.URL

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.core.views.www_detail', [self.pk])

	def	get_edit_url(self):
		return reverse('apps.core.views.www_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.core.views.www_del', args=[self.pk])

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'WWW'
		verbose_name_plural	= u'WWW'
		ordering		= ('URL',)

class	Email(Object):
	'''
	E-mail
	RFC:
	internet	- an Internet addressing type
	x400		- a X.400 addressing type
	pref		- a preferred-use email address when more than one is specified.
	'''
	URL		= models.EmailField(unique=True, verbose_name=u'Email')

	def	__unicode__(self):
		return self.URL

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.core.views.email_detail', [str(self.pk)])

	def	get_edit_url(self):
		return reverse('apps.core.views.email_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.core.views.email_del', args=[self.pk])

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'E-mail'
		verbose_name_plural	= u'E-mail'
		ordering		= ('URL',)

class	IMType(models.Model):
	'''
	Тип IM: GTalk, AIM, Yahoo, Skype, QQ, MSN, ICQ, Jabber
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name=u'Аббревиатура')
	comments	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Комментарии')

	def	__unicode__(self):
		return self.name

	class	Meta:
		app_label		= 'gw'
		ordering		= ('id', )
		verbose_name		= u'Тип IM'
		verbose_name_plural	= u'Типы IM'

class	IM(Object):
	account		= models.CharField(max_length=64, null=False, blank=False, verbose_name=u'Учетная запись')
	type		= models.ForeignKey(IMType, null=False, blank=False, verbose_name=u'Тип')

	def	__unicode__(self):
		return u'%s: %s' % (self.type.name, self.account)

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.core.views.im_detail', [str(self.pk)])

	def	get_edit_url(self):
		return reverse('apps.core.views.im_edit', args=[self.pk])

	def	get_del_url(self):
		return reverse('apps.core.views.im_del', args=[self.pk])

	class	Meta:
		app_label		= 'gw'
		verbose_name		= u'IM'
		verbose_name_plural	= u'IM'
		ordering		= ('type', 'account',)
		unique_together		= (('account', 'type',),)
