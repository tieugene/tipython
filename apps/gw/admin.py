# -*- coding: utf-8 -*-
'''
lansite.gw.admin.py
'''

from django.contrib import admin
from models import *

from bits.admin import *
from contact.models import *
from task.models import *
#from task.admin import *
from file.admin import *
from tagged.models import *
from tagged.admin import *

# 1. inlines

class	WordCombinationInLine(admin.TabularInline):
    model		= WordCombination
    extra		= 1

    
class	WordCombinationAdmin(admin.ModelAdmin):
  #  list_display	= ('high', 'name',)
    ordering	= ('nominative',)
    search_field	= ('nominative',)

admin.site.register(WordCombination, WordCombinationAdmin)