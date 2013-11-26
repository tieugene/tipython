# -*- coding: UTF-8 -*-

__author__ = 'sdv'


from django.contrib import admin
from clients.models import Client, Person, Document, Phone, Email, Adress, Stuff,Employee,Speciality,Education,SkillLevel,EMC,ClientCategory,Disability,Positions

class EmailInline(admin.StackedInline):
    model = Email
    extra = 2

class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 2


class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (u'ФИО:',           {'fields':  ['lastName', 'firstName', 'middleName']}),
        (u'Контакты:',      {'fields':  ['phone','email']}),
        (u'Дополнительная информация:',        {'fields':  ['birthDate','passport','inn','snils'], 'classes': ['collapse']}),
    ]
#    inlines = [EmailInline, PhoneInline]
    list_display = ('get_fio','birthDate','phone','email')
    list_filter = ['lastName','birthDate']
    search_fields = ['lastName']
    date_hierarchy = 'birthDate'
    


admin.site.register(Client)
#admin.site.register(Client,ClientAdmin)
admin.site.register(Person)
admin.site.register(Document)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(Adress)
admin.site.register(Stuff)
admin.site.register(Employee)
admin.site.register(Speciality)
admin.site.register(Education)
admin.site.register(SkillLevel)
admin.site.register(EMC)
admin.site.register(ClientCategory)
admin.site.register(Disability)
admin.site.register(Positions)



