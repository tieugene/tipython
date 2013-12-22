# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class   BillEventInLine(admin.TabularInline):
        model           = BillEvent
        extra           = 1

class   ApproverInLine(admin.TabularInline):
        model           = Approver
        extra           = 1

# 2. odmins
class	BillAdmin(admin.ModelAdmin):
	#ordering	= ('pk',)
	list_display	= ('project', 'depart', 'assign', 'approve', 'isalive', 'isgood')
	inlines		= [BillEventInLine,]

class	ApproverAdmin(admin.ModelAdmin):
	ordering	= ('user',)
	list_display	= ('user', 'role',)

class	RoleAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'name')
	inlines		= [ApproverInLine,]

admin.site.register(Bill,	BillAdmin)
admin.site.register(Approver,	ApproverAdmin)
admin.site.register(Role,	RoleAdmin)
