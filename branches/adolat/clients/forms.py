# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from django.views.generic import FormView, ListView,  DetailView
from django.forms import ModelForm
from clients.models import Client

class AddClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['personType','timestamp','lastName','firstName','middleName','birthDate','birthPlace','gender','inn','enp','snils','emc','disabilityFlag','disability','source_of_treatment','educationType','category','bloodType']




class ClientFormView(FormView):
    class Meta:
        model = Client


class ClientListView(ListView):
    class Meta:
        model = Client

class ClientDetailView(DetailView):
    class Meta:
        model = Client
