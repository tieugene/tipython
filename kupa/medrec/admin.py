# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class	RecordInLine(admin.TabularInline):
        model	= Record
        extra	= 1
	#fields	= ('date', 'time')

# 2. odmins
class	ClientAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'lname', 'fname', 'mname', 'comment')
	#exclude		= ('name', 'size', 'md5', 'mime')
	inlines		= (RecordInLine,)

class	RecordAdmin(admin.ModelAdmin):
	ordering	= ('date', 'time', 'client')
	list_display	= ('id', 'date', 'time', 'client', 'durat', 'comment', 'code', 'state')
	#exclude		= ('name', 'size', 'md5', 'mime')
	#inlines		= (RecordInLine,)

admin.site.register(Client,	ClientAdmin)
admin.site.register(Record,	RecordAdmin)
