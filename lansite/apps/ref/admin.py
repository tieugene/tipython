# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from treebeard.admin import TreeAdmin
from models import *

# 1. Inlines

# 2. Odmins

class	OkatoAdmin(TreeAdmin):
	list_display	= ('id', 'name',)
	ordering	= ('id',)

class	OkopfAdmin(TreeAdmin):
	list_display	= ('id', 'name', 'shortname', 'disabled')
	ordering	= ('id',)

class	OksmAdmin(admin.ModelAdmin):
	list_display	= ('id', 'alpha2', 'alpha3', 'name', 'fullname')
	ordering	= ('name',)
	search_fields	= ('name',)

class	KladrShortAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name', 'fullname')
	ordering	= ('name',)
	search_fields	= ('name',)

class	KladrStateTypeAdmin(admin.ModelAdmin):
	list_display	= ('id', 'comments')
	ordering	= ('id',)
	search_fields	= ('id',)

class	KladrAdmin(admin.ModelAdmin):
	list_display	= ('id', 'name')
	ordering	= ('id',)
	search_fields	= ('name',)

admin.site.register(KladrShort,		KladrShortAdmin)
admin.site.register(KladrStateType,	KladrStateTypeAdmin)
admin.site.register(Kladr,		KladrAdmin)
admin.site.register(Okopf,		OkopfAdmin)
admin.site.register(Oksm,		OksmAdmin)
admin.site.register(Okato,		OkatoAdmin)
admin.site.register(Okved,		admin.ModelAdmin)
