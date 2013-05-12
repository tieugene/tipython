# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines

class	ContactAddrInLine(admin.TabularInline):
	model		= ContactAddr
	extra		= 1

class	ContactPhoneInLine(admin.TabularInline):
	model		= ContactPhone
	extra		= 1

class	ContactWWWInLine(admin.TabularInline):
	model		= ContactWWW
	extra		= 1

class	ContactEmailInLine(admin.TabularInline):
	model		= ContactEmail
	extra		= 1

class	ContactIMInLine(admin.TabularInline):
	model		= ContactIM
	extra		= 1

class	PersonInLine(admin.TabularInline):
	model		= Person
	extra		= 1

class	OrgInLine(admin.TabularInline):
	model		= Org
	extra		= 1

class	OrgStuffInLine(admin.TabularInline):
	model		= OrgStuff
	extra		= 1

# 2. odmins

class	ContactAdmin(admin.ModelAdmin):
	inlines		= (ContactAddrInLine, ContactPhoneInLine, ContactWWWInLine, ContactEmailInLine, ContactIMInLine,)

class	PersonAdmin(admin.ModelAdmin):
	inlines		= (ContactAddrInLine, ContactPhoneInLine, ContactWWWInLine, ContactEmailInLine, ContactIMInLine,)

class	OrgAdmin(admin.ModelAdmin):
	inlines		= (ContactAddrInLine, ContactPhoneInLine, OrgStuffInLine, ContactWWWInLine, ContactEmailInLine, ContactIMInLine,)

admin.site.register(Contact,		ContactAdmin)
admin.site.register(ContactAddrType,	admin.ModelAdmin)
admin.site.register(Org,		OrgAdmin)
admin.site.register(Person,		PersonAdmin)
admin.site.register(JobRole,		admin.ModelAdmin)
