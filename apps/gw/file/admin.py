# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines

# 2. odmins

admin.site.register(File,	admin.ModelAdmin)
admin.site.register(ImageFile,	admin.ModelAdmin)
