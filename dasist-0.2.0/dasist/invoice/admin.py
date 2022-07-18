from django.contrib import admin

from . import models


# 1. inlines
class RouteInLine(admin.TabularInline):
    model = models.Route
    extra = 1


class EventInLine(admin.TabularInline):
    model = models.Event
    extra = 1


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    ordering = ('fileseq',)
    list_display = ('fileseq', 'shipper', 'shipper', 'assign', 'rpoint', 'state',)
    inlines = (RouteInLine, EventInLine,)
