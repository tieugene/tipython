# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class	ToDoInLine(admin.TabularInline):
	model		= ToDo
	extra		= 1

class	AssignInLine(admin.TabularInline):
	model		= Assign
	extra		= 1

# 2. odmins
class	ToDoCatAdmin(admin.ModelAdmin):
	inlines		= (ToDoInLine,)

class	AssignCatAdmin(admin.ModelAdmin):
	inlines		= (AssignInLine,)

admin.site.register(Task,		admin.ModelAdmin)
admin.site.register(ToDoCat,		ToDoCatAdmin)
admin.site.register(ToDo,		admin.ModelAdmin)
admin.site.register(AssignCat,		AssignCatAdmin)
admin.site.register(Assign,		admin.ModelAdmin)
