# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from django.http import HttpResponseRedirect
#from django.template import RequestContext, loader
from clients.models import Client
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import Http404
from django.core.urlresolvers import reverse
from clients import forms

def index(request):
    try:
        latest_client_list = Client.objects.order_by('-lastName')[:50]
        context =  {'latest_client_list': latest_client_list}
    except Client.DoesNotExist:
        raise Http404
    return render(request, 'clients/list.html',context)

def detail(request, client_id):
    client = get_object_or_404(Client,pk=client_id)
    return render(request, 'clients/detail.html',{'client': client})

def edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    try:
        #customer.lastName = request.POST['lastName']
        #customer.firstName = request.POST['firstName']
        #customer.middleName = request.POST['middleName']
        #customer.inn = request.POST['inn']
        #customer.snils = request.POST['snils']

        #selected_phone = customer.phone_set.get

        phone = client.phone.get(pk=request.POST['phone_id'])
        #phone.number = request.POST['phone']
        #p = phone.client_set
        #customer.lastName = request.POST['lastName']
        #customer.lastName = request.POST['lastName']
        #selected_customer = customer.choice_set.get(pk=request.POST['choice'])
        selected_client = client.id         #get(pk=request.POST['choice'])
    except (KeyError, Client.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'clients/list.html', { 'client': client,
            'error_message': "You didn’t select anything.",
            })
    else:
        #selected_choice.votes += 1
        #selected_choice.save()
        client.save()
        # Always return an HttpResponseRedirect after successfully dealing # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('clients.views.updated', args=(client.id,)))

def updated(request, client_id):
    client = get_object_or_404(Client,pk=client_id)
    return render(request, 'clients/updated.html',{'client': client})

def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = forms.AddClientForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            client = form.save()
            #client = Client.objects.create()
            # Process the data in form.cleaned_data
            # ...
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']
            return HttpResponseRedirect(reverse('clients.views.updated', args=(client.id,))) # Redirect after POST
    else:
        form = forms.AddClientForm(auto_id=True) # An unbound form

    return render(request, 'clients/client.html', {'form': form,})

def remove(request, client_id):
    client = get_object_or_404(Client,pk=client_id)
    return render(request, 'clients/updated.html',{'client': client})

# TODO: Добавить jQuery UI виджеты для выбора даты и формата даты и телефона
# TODO: Добавить иконки для выбора действий в списке клиентов

