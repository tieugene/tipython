from django.contrib import admin
from . import models


@admin.register(models.Org)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'inn', 'name', 'fullname')
    ordering = ('name',)


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    ...


class ApproverInline(admin.TabularInline):
    model = models.Approver
    extra = 1


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    inlines = (ApproverInline,)


@admin.register(models.Approver)
class ApproverAdmin(admin.ModelAdmin):
    ...


class SubjectInline(admin.TabularInline):
    model = models.Subject
    extra = 1


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    inlines = (SubjectInline,)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Payer)
class PayerAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
