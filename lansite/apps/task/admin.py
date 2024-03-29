# -*- coding: utf-8 -*-
from django.contrib import admin
from objectpermissions.admin import TabularUserPermInline, TabularGroupPermInline, StackedUserPermInline, StackedGroupPermInline
from models import *

# 1. inlines
class	CategoryInLine(admin.TabularInline):
	model		= Category
	extra		= 1

class	TaskInLine(admin.TabularInline):
	model		= Task
	extra		= 1

class	TaskCatInLine(admin.TabularInline):
	model		= TaskCat
	extra		= 1

# 2. odmins
class	CategoryAdmin(admin.ModelAdmin):
	list_display	= ('name', 'user', 'app',)
	inlines		= (TaskCatInLine, TabularUserPermInline, TabularGroupPermInline)

class	TaskAdmin(admin.ModelAdmin):
	inlines		= (TaskCatInLine,)

class	vToDoAdmin(admin.ModelAdmin):
	list_display	= ('summary', 'user', 'attendee',)
	inlines		= (TaskCatInLine, TabularUserPermInline, TabularGroupPermInline)

admin.site.register(Category,		CategoryAdmin)
admin.site.register(Task,		TaskAdmin)
admin.site.register(vToDo,		vToDoAdmin)
admin.site.register(vEvent,		admin.ModelAdmin)
