# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines

class	ODFExportInLine(admin.TabularInline):
	model		= ODFExport
	extra		= 1

class	DocTypeInLine(admin.TabularInline):
	model		= DocType
	extra		= 1

class	DocEntityInLine(admin.TabularInline):
	model		= DocEntity
	extra		= 1

# 2. odmins

class	ODFTypeAdmin(admin.ModelAdmin):
	inlines		= (ODFExportInLine, DocTypeInLine)
	ordering	= ('id',)
	list_display	= ('id', 'name',)

class	ODFExportAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'odftype', 'name',)

class	DocTypeAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'name', 'desc',)

class	DocEntityAdmin(admin.ModelAdmin):
	ordering	= ('name',)
	list_display	= ('name',)

admin.site.register(ODFType,	ODFTypeAdmin)
admin.site.register(ODFExport,	ODFExportAdmin)
admin.site.register(DocType,	DocTypeAdmin)
admin.site.register(DocEntity,	DocEntityAdmin)
