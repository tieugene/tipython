# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
#from treebeard.admin import TreeAdmin

class	DocAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'user', 'type', 'name', 'created', 'updated')

class	LogAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'date', 'method', 'ip', 'path', 'agent')

class	SSRFAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'name')

class	OkvedAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'parent', 'name')

admin.site.register(Doc,	DocAdmin)
admin.site.register(Log,	LogAdmin)
admin.site.register(SSRF,	SSRFAdmin)
admin.site.register(Okved,	OkvedAdmin)
