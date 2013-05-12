# -*- coding: utf-8 -*-
'''
lansite.apps.file.views
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext
# generic views
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

# 2. python
from datetime import datetime
import sys, xml.dom

# 3. my
from models import *
from forms import *
import webdav

# 4. siblings
from apps.eav.forms import TypeListForm
from apps.eav.models import TaggedObjectTag

PAGE_SIZE = 20

@login_required
def	index(request):
	print "Index:"
	if (request.method == 'OPTIONS'):
		print "root OPTIONS"
		response = HttpResponse(content_type = 'httpd/unix-directory')
		response['Allow'] = 'OPTIONS,GET,PUT,HEAD,POST'
		return response
	#return render_to_response('file/index.html', context_instance=RequestContext(request))
	return direct_to_template(request, 'file/index.html')

@login_required
def	file_index(request):
	#return render_to_response('file/list.html', context_instance=RequestContext(request, { 'item_list': File.objects.all(), 'form': FileAddForm() }))
	return	object_list (
		request,
		queryset = File.objects.all(),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'file/file_list.html',
		extra_context = {
			'form': FileAddForm(),
		}
	)

@login_required
def	file_index_img(request):
	#return render_to_response('file/image_list.html', context_instance=RequestContext(request, { 'item_list': ImageFile.objects.all(), 'form': FileAddForm() }))
	return	object_list (
		request,
		queryset = ImageFile.objects.all(),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
		template_name = 'file/image_list.html',
		extra_context = {
			'form': FileAddForm(),
		}
	)

@login_required
def	file_detail(request, object_id):
	if (File.objects.get(pk=object_id).get_real_instance_class() == ImageFile):
		return file_detail_img(request, object_id)
	#return render_to_response('file/file_detail.html', context_instance=RequestContext(request, {'item': file}))
	return	object_detail (
		request,
		queryset = File.objects.all(),
		object_id = object_id,
		template_name = 'file/file_detail.html',
	)

@login_required
def	file_detail_img(request, object_id):
	'''
	TODO: preview (bmp?, gif, ?ico, jpg, png) or tiff=>gif/jpg/png (1-bit, max 512)
	'''
	#file = ImageFile.objects.get(pk=item_id)
	#return render_to_response('file/image_detail.html', context_instance=RequestContext(request, {'item': file}))
	return	object_detail (
		request,
		queryset = ImageFile.objects.all(),
		object_id = object_id,
		template_name = 'file/image_detail.html',
	)

@login_required
def	file_add(request):
	if request.method == 'POST':
		f = FileAddForm(request.POST, request.FILES)
		if f.is_valid():
		    file = request.FILES['file']
		    content_type = request.FILES['file'].content_type.split('/', 1)[0]
		    if (content_type == 'image'):
			ImageFile(file=file).save()
		    else:
			File(file=file).save()
	return redirect('apps.file.views.file_index')
	#return HttpResponseRedirect(reverse('apps.file.views.file_index'))

@login_required
def	file_edit(request, object_id):
	'''
	item = File.objects.get(pk=object_id)
	if request.method == 'POST':
		f = FileEditForm(request.POST, instance=item)
		if f.is_valid():
			f.save()
	else:    # GET
		f = FileEditForm(instance=item)
	return render_to_response('file/file_edit.html', context_instance=RequestContext(request, {'item': item, 'form': f}))
	'''
	return	update_object (
		request,
		form_class = FileEditForm,
		object_id = object_id,
		template_name = 'file/file_form.html',	# FIXME: 
	)

@login_required
def	file_del(request, object_id):
	TaggedObjectTag.objects.filter(value=object_id).delete()
	File.objects.get(pk=object_id).delete()
	return redirect('apps.file.views.file_index')

@login_required
def	file_dl(request, object_id):    #def    file_dl(request, file_id, file_name):
	'''
	web.header("Content-Type", "%s/%s;" % (item.mime_media, item.mime_type))
	web.header("Content-Transfer-Encoding" , "binary");
	web.header("Content-Disposition", "attachment; filename=\"%s\";" % item.origfn);
	web.header("Content-Length", "%d" % item.size);
	return open(os.path.join(config.filepath, "%08X" % (int(item.id)))).read()
	'''
	file = File.objects.get(id=long(object_id))
	response = HttpResponse(content_type = file.mime)    # HttpResponse(mimetype='text/xml; charset=utf-8')
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = (u'attachment; filename=\"%s\";' % file.name).encode('utf-8')
	response.write(open(file.file.path).read())
	return response

def	dav(request):
	'''
	'''
	print request.method
	func = webdav.davdict.get(request.method, None)
	if func:
		return func(request)
	else:
		raise Http404
