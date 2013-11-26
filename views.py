# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
