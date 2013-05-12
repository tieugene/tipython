# -*- coding: utf-8 -*-
'''
lansite.gw.views.py
'''

# 1. django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from bits.views import *
from contact.views import *
#from task.views import *
from file.views import *
from address.views import *
from forms import *
from apps.sro2.forms import OrgInsuranceForm
from django.contrib.auth.models import Group
from apps.sro2.jnj import render_to

@login_required
def    gw_context(context):
    '''
    '''
    return {'menus': ("gw/menu.html", "sro2/menu.html")} # temprary fix. i think, this way is better.

@login_required
def	index(request):
    #return render_to_response('gw/index.html')
    #if not request.user.is_authenticated():
    #return HttpResponseRedirect('../login/?next=%s' % request.path)
    #return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
    #return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
    return render_to_response('gw/index.html', RequestContext(request, {'menus': (
        'gw/menu.html',
    )}))

from sro2.jnj import *
from sro2.shared import superuser_only

@render_to("gw/wordcombination_list.html")
def wordcombination_list(request):
    wordcombinations=WordCombination.objects.all().order_by('nominative')
    return {
        'wordcombinations':wordcombinations,
    }

@render_to("gw/wordcombination_edit.html")
def wordcombination_edit(request, wordcombination_id):
    wordcombination = WordCombination.objects.get(id=wordcombination_id)
    if request.method == 'POST':
        form = WordCombinationEditForm(request.POST, instance=wordcombination)
        if form.is_valid():
            wordcombination = form.save()
            return redirect(wordcombination_list)
    else:
        form = WordCombinationEditForm(instance=wordcombination)
    return {
        'wordcombination':wordcombination,
        'form': form,
    }

@render_to("gw/wordcombination_add.html")
def wordcombination_add(request):
    if request.method == 'POST':
        form = WordCombinationEditForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.save()
            return redirect(wordcombination_list)
    else:
        form = WordCombinationEditForm()
    return {
        'form': form,
    }

def wordcombination_delete(request, wordcombination_id):

    wordcombination = WordCombination.objects.get(id=wordcombination_id)
    wordcombination.delete()
    return redirect(wordcombination_list)

@superuser_only
@render_to("gw/permission_list.html")
def permission_list(request):
    list = [
            'person',
            'org',
            'orgsro',
            'permit',
            'statement',
    ]
    forms = {}
    contenttypes = ContentType.objects.filter(model__in=list)
    for contenttype in contenttypes:
        form = PermissionAddForm()
        form.setdata(contenttype.id)
        forms[contenttype.id] = form

    
    return {
        'contenttypes': contenttypes,
        'forms': forms,
    }

@superuser_only
@render_to("gw/permission_.html")
def permission_add(request):
    list = [
        'statement',
        'org',
        'orgsro',
        'permit',
        'person',
    ]
    contenttypes = ContentType.objects.filter(model__in=list)
    groups = Group.objects.all()
    return {
        'contenttypes': contenttypes,
        'groups': groups,
    }

@superuser_only
@render_to('gw/permission_table.html')
def permission_gettable(request, number):
    list = [
        'statement',
        'org',
        'orgsro',
        'permit',
        'person',
    ]

    contenttype = ContentType.objects.get(model=list[int(number)])


    permissions = Permissions.objects.filter(model__id=contenttype.id, is_user=False).values('subject')
    groups = Group.objects.filter(~Q(id__in=permissions)).values_list('name', flat=True)
    permissions1 = Permissions.objects.filter(model__id=contenttype.id, is_user=False)

    permissions2 = Permissions.objects.filter(model__id=contenttype.id, is_user=True)
    #dd = set(permissions)


    permissions = Permissions.objects.filter(model__id=contenttype.id, is_user=False).values('subject')
    permissions22 = Permissions.objects.filter(model__id=contenttype.id, is_user=True).values('subject')
    groups = Group.objects.filter(~Q(id__in=permissions)).order_by('name')
    users = User.objects.filter(~Q(id__in=permissions22)).order_by('first_name', 'last_name')
    return {'permissions': permissions1, 'groups':groups, 'permissions1': permissions2, 'users': users,}

@superuser_only
def permission_save(request, contenttype_id):
    return HttpResponse('dsd');
