# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class	RIPEAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	#list_display	= ('id', 'user', 'type', 'name', 'created', 'updated')

admin.site.register(RIPE,	RIPEAdmin)
