from django.contrib import admin

from . import models


# 1. inlines
class RouteInLine(admin.TabularInline):
    model = models.Route
    extra = 1


class EventInLine(admin.TabularInline):
    model = models.Event
    extra = 1


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    ordering = ('fileseq',)
    list_display = ('fileseq', 'payer', 'shipper', 'assign', 'state',)
    inlines = (RouteInLine, EventInLine,)
