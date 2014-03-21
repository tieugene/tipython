# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines

# 2. odmins
class	FileAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'name', 'size', 'md5')
	exclude		= ('name', 'size', 'md5', 'mime')

admin.site.register(File,	FileAdmin)
