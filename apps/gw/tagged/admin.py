# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
from apps.gw.tagged.models import *

# 1. inlines
class	TaggedObjectTagTypeInLine(admin.TabularInline):
	model		= TaggedObjectTagType
	extra		= 1

class	TaggedObjectTypeInLine(admin.TabularInline):
	model		= TaggedObjectType
	extra		= 1

# 2. odmins
class	TaggedObjectTypeAdmin(admin.ModelAdmin):
	inlines		= (TaggedObjectTagTypeInLine,)

class	TaggedObjectAdmin(admin.ModelAdmin):
	inlines		= (TaggedObjectTagTypeInLine,)

admin.site.register(TaggedObjectTagType,	admin.ModelAdmin)
admin.site.register(TaggedObjectType,		TaggedObjectTypeAdmin)
admin.site.register(TaggedObjectTag,		admin.ModelAdmin)
admin.site.register(TaggedObject,		TaggedObjectAdmin)
