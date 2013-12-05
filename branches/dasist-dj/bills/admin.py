# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class   BillRouteInLine(admin.TabularInline):
        model           = BillRoute
        extra           = 1

class   BillEventInLine(admin.TabularInline):
        model           = BillEvent
        extra           = 1

# 2. odmins
class	BillAdmin(admin.ModelAdmin):
	#ordering	= ('pk',)
	list_display	= ('project', 'depart', 'assign', 'approve', 'isalive', 'isgood')

class	ApproverAdmin(admin.ModelAdmin):
	ordering	= ('user',)
	list_display	= ('user', 'role',)

class	RoleAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'name')

admin.site.register(Bill,	BillAdmin)
admin.site.register(Approver,	ApproverAdmin)
admin.site.register(Role,	RoleAdmin)
