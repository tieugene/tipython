# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

from apps.gw.contact.admin import ContactPhoneInLine, ContactWWWInLine, ContactEmailInLine, ContactIMInLine
 
# 1. inlines

'''
class	SubObjectInLine(admin.TabularInline):
	model		= SubObject
	extra		= 1
'''

class	AddrInLine(admin.TabularInline):
	model		= Address
	extra		= 1

# 2. odmins

class	ObjectAdmin(admin.ModelAdmin):
	pass
	'''
	inlines		= (SubObjectInLine,)
	'''

class	UserSettingAdmin(admin.ModelAdmin):
	list_display	= ('user', 'form', 'action', 'object', 'value')

class	PhoneAdmin(admin.ModelAdmin):
	inlines		= (ContactPhoneInLine,)

class	WWWAdmin(admin.ModelAdmin):
	inlines		= (ContactWWWInLine,)

class	EmailAdmin(admin.ModelAdmin):
	inlines		= (ContactEmailInLine,)

class	IMAdmin(admin.ModelAdmin):
	inlines		= (ContactIMInLine,)

class	AddrAdmin(admin.ModelAdmin):
	inlines		= (AddrInLine,)

admin.site.register(GwUser,		admin.ModelAdmin)
admin.site.register(Object,		ObjectAdmin)
admin.site.register(UserSetting,	UserSettingAdmin)
admin.site.register(AddrType,		admin.ModelAdmin)
admin.site.register(AddrShort,		admin.ModelAdmin)
admin.site.register(Address,		admin.ModelAdmin)
admin.site.register(PhoneType,		admin.ModelAdmin)
admin.site.register(Phone,		PhoneAdmin)
admin.site.register(WWW,		WWWAdmin)
admin.site.register(Email,		EmailAdmin)
admin.site.register(IMType,		admin.ModelAdmin)
admin.site.register(IM,			IMAdmin)

