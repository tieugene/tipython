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

class	OkatoInLine(admin.TabularInline):
    model		= Okato
    extra		= 1

class	OkopfInLine(admin.TabularInline):
    model		= Okopf
    extra		= 1

class	OkvedInLine(admin.TabularInline):
    model		= Okved
    extra		= 1

class	SpecialityInLine(admin.TabularInline):
    model		= Speciality
    extra		= 1

class	SkillInLine(admin.TabularInline):
    model		= Skill
    extra		= 1

class	RoleInLine(admin.TabularInline):
    model		= Role
    extra		= 1

class	PersonSkillInLine(admin.TabularInline):
    model		= PersonSkill
    extra		= 1

class	OrgOkvedInLine(admin.TabularInline):
    model		= OrgOkved
    extra		= 1
    raw_id_fields	= ('okved',)

# 2. odmins

class	ContactAdmin(admin.ModelAdmin):
    inlines		= (ContactAddrInLine, ContactPhoneInLine, ContactWWWInLine, ContactEmailInLine, ContactIMInLine,)

class	PersonAdmin(admin.ModelAdmin):
    inlines		= (PersonSkillInLine, OrgStuffInLine,)
    list_display	= ('lastname', 'firstname', 'midname',)
    ordering	= ('lastname', 'firstname', 'midname',)

class	OrgAdmin(admin.ModelAdmin):
    inlines		= ()

class	OkatoAdmin(admin.ModelAdmin):
    list_display	= ('id', 'name')
    ordering	= ('id',)
    search_fields	= ('name',)

class	OkopfAdmin(admin.ModelAdmin):
    list_display	= ('id', 'name', 'shortname', 'namedp', 'disabled', 'parent')
    ordering	= ('id',)
    search_fields	= ('shorname',)
    inlines		= (OkopfInLine,)

class	OkvedAdmin(admin.ModelAdmin):
    list_display	= ('id', 'name', 'parent')
    ordering	= ('id',)
    search_fields	= ('name',)
    inlines		= (OkvedInLine,)

class	SpecialityAdmin(admin.ModelAdmin):
    list_display	= ('name',)
    ordering	= ('name',)
    search_fields	= ('name',)
    inlines		= (PersonSkillInLine,)

class	SkillAdmin(admin.ModelAdmin):
    list_display	= ('high', 'name',)
    ordering	= ('high', 'name',)
    search_field	= ('name',)
    inlines		= (PersonSkillInLine,)

class	RoleAdmin(admin.ModelAdmin):
    list_display	= ('name', 'comments')
    ordering	= ('name',)

admin.site.register(Contact,		ContactAdmin)
admin.site.register(ContactAddrType,	admin.ModelAdmin)
admin.site.register(Org,		OrgAdmin)
admin.site.register(Person,		PersonAdmin)
admin.site.register(Role,		admin.ModelAdmin)
admin.site.register(Okato,		OkatoAdmin)
admin.site.register(Okopf,		OkopfAdmin)
admin.site.register(Okved,		OkvedAdmin)
admin.site.register(Speciality,		SpecialityAdmin)
admin.site.register(Skill,		SkillAdmin)

