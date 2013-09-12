# -*- coding: utf-8 -*-

# 1. django
from django.db import models
from django.contrib.auth.models import User

# 2. my

# 3. 3rds
from iptools.ipv4 import long2ip

# 4. system
import datetime


class   RIPE(models.Model):
	id		= models.BigIntegerField(primary_key=True, verbose_name=u'ID')
	beg		= models.PositiveIntegerField(null=False, db_index=True, verbose_name=u'IP net')
	end		= models.PositiveIntegerField(null=False, db_index=True, verbose_name=u'IP broadcast')
	#mtime		= models.DateTimeField(null=False, db_index=True, verbose_name=u'Изменен')		# editable-False

	def     __unicode__(self):
		return '%s - %s' % (long2ip(self.beg), long2ip(self.end))

	def get_beg(self):
		return (long2ip(self.beg))

	def get_end(self):
		return (long2ip(self.end))

	@models.permalink
	def get_absolute_url(self):
		return ('az.views.ripe_detail', [str(self.id)])

	#def get_edit_url(self):
	#	return reverse('az.views.doc_u', args=[self.pk])

	#def get_del_url(self):
	#	return reverse('az.views.doc_d', args=[self.pk])

	class   Meta:
		db_table = 'ripe'
		ordering                = ('beg', 'end')
		verbose_name            = u'Сеть'
		verbose_name_plural     = u'Сети'

class   RIPEc(models.Model):
	id		= models.BigIntegerField(primary_key=True, verbose_name=u'ID')
	ripe		= models.ForeignKey(RIPE, db_index=True, verbose_name=u'Net')
	c		= models.PositiveIntegerField(null=False, db_index=True, verbose_name=u'#')
	k		= models.CharField(null=False, db_index=True, max_length=15, verbose_name=u'Key')
	v		= models.CharField(null=False, db_index=True, max_length=255, verbose_name=u'Value')

	def     __unicode__(self):
		return self.id

	class   Meta:
		db_table = 'ripec'
		ordering                = ('ripe', 'c')
		verbose_name            = u'Атрибут сети'
		verbose_name_plural     = u'Атрибуты сети'
