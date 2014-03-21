# -*- coding: utf-8 -*-
'''
'''

# 1. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile

# 4. my
import models, forms

import os

PAGE_SIZE = 20

def	file_list(request):
	return  object_list (
		request,
		queryset = models.File.objects.all(),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'filer/list.html',
	)

def	file_add(request):
	if request.method == 'POST':
		form = forms.FileAddForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			filename = file.name
			filepath = os.path.join(settings.MEDIA_ROOT, filename)
			#myfile = File(file=SimpleUploadedFile(filename, default_storage.open(filename).read()))
			#myfile = models.File(file=SimpleUploadedFile(filename, open(filepath).read()))	# unicode error
			myfile = models.File(file=file)	# unicode error
			myfile.save()
			return redirect('filer.views.file_list')
	else:
		form = forms.FileAddForm()
	return render_to_response('filer/form.html', context_instance=RequestContext(request, {'form': form,}))

def	file_view(request, id):
        return  object_detail (
                request,
                queryset = models.File.objects.all(),
                object_id = id,
                template_name = 'filer/view.html',
        )

def	file_get(request, id):
	file = models.File.objects.get(pk=int(id))
	response = HttpResponse(mimetype=file.mime)
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = '; filename=\"%s\"' % file.name.encode('utf-8')
	response.write(open(file.get_path()).read())
	return response

def	file_edit(request, id):
	item = models.file.objects.get(pk=int(id))

def	file_del(request, id):
	item = models.File.objects.get(pk=int(id)).delete()
	return redirect('filer.views.file_list')
