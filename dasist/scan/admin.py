# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines

# 2. odmins
class	ScanAdmin(admin.ModelAdmin):
	ordering	= ('date',)
	list_display	= ('project', 'depart', 'supplier', 'no', 'date')

admin.site.register(Scan,	ScanAdmin)
