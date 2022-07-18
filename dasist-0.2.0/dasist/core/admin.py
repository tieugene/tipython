from django.contrib import admin

from . import models


# 1. inlines
class FileSeqItemInLine(admin.TabularInline):
    model = models.FileSeqItem
    extra = 1
    fields = ('order', 'file')


# 2. odmins
@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    """
    TODO:
    - add: file only
    - edit/view: name only
    """
    ordering = ('id',)
    list_display = ('id', 'name', 'size', 'ctime', 'mime')
    # exclude = ('name', 'size', 'md5', 'mime')
    readonly_fields = ('id', 'size', 'ctime', 'mime', 'md5')
    inlines = (FileSeqItemInLine,)


@admin.register(models.FileSeq)
class FileSeqAdmin(admin.ModelAdmin):
    ordering = ('id',)
    inlines = (FileSeqItemInLine,)
