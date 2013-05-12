# -*- coding: utf-8 -*-
'''
lansite.gw.task.views.py
'''

# 1. django
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import loader, Context, RequestContext

# 2. python
from datetime import datetime
import sys

# 3. my
from models import *
from forms import *

# 4. siblings
from apps.gw.tagged.forms import TypeListForm
from apps.gw.tagged.models import TaggedObjectTag

@login_required
def    file_index(request):
	return render_to_response('gw/file/index.html', context_instance=RequestContext(request))

@login_required
def    file_index_all(request):
    return render_to_response('gw/file/index_all.html', context_instance=RequestContext(request, {
        'item_list': File.objects.all(),
        'form': FileAddForm()
    }))

@login_required
def    file_index_img(request):
    '''
    '''
    return render_to_response('gw/file/index_img.html', context_instance=RequestContext(request, {
        'item_list': ImageFile.objects.all(),
        'form': FileAddForm()
    }))

@login_required
def    file_add(request):
    if request.method == 'POST':
        f = FileAddForm(request.POST, request.FILES)
        if f.is_valid():
            file = request.FILES['file']
            content_type = request.FILES['file'].content_type.split('/', 1)[0]
            #print content_type
            if (content_type == 'image'):
                ImageFile(file=file).save()
            else:
                File(file=file).save()
    return HttpResponseRedirect(reverse('gw.views.file_index'))

@login_required
def    file_detail(request, item_id):
    file = File.objects.get(pk=item_id)
    if (file.get_real_instance_class() == ImageFile):
        return file_detail_img(request, item_id)
    return render_to_response('gw/file/detail.html', context_instance=RequestContext(request, {'item': file}))

@login_required
def    file_detail_img(request, item_id):
    '''
    TODO: preview (bmp?, gif, ?ico, jpg, png) or tiff=>gif/jpg/png (1-bit, max 512)
    '''
    file = ImageFile.objects.get(pk=item_id)
    return render_to_response('gw/file/detail_img.html', context_instance=RequestContext(request, {'item': file}))

@login_required
def    file_edit(request, item_id):
    #print "edit"
    item = File.objects.get(pk=item_id)
    if request.method == 'POST':
        f = FileEditForm(request.POST, instance=item)
        if f.is_valid():
            f.save()
    else:    # GET
        f = FileEditForm(instance=item)
    return render_to_response('gw/file/edit.html', context_instance=RequestContext(request, {'item': item, 'form': f}))

@login_required
def    file_del(request, item_id):
    TaggedObjectTag.objects.filter(value=item_id).delete()
    File.objects.get(pk=item_id).delete()
    return HttpResponseRedirect(reverse('gw.views.file_index'))

@login_required
def    file_dl(request, item_id):    #def    file_dl(request, file_id, file_name):
    '''
    web.header("Content-Type", "%s/%s;" % (item.mime_media, item.mime_type))
    web.header("Content-Transfer-Encoding" , "binary");
    web.header("Content-Disposition", "attachment; filename=\"%s\";" % item.origfn);
    web.header("Content-Length", "%d" % item.size);
    return open(os.path.join(config.filepath, "%08X" % (int(item.id)))).read()
    '''
    file = File.objects.get(id=int(item_id))
    response = HttpResponse(content_type = file.mime)    # HttpResponse(mimetype='text/xml; charset=utf-8')
    response['Content-Transfer-Encoding'] = 'binary'
    # FIXME: django.http.__init__.py: ..._convert_to_ascii: value.encode('us-ascii') -> 'utf-8'
    #response['Content-Disposition'] = u'attachment; filename=\"%s\";' % file.name
    #response['Content-Disposition'] = 'attachment; filename=\"%s\";' % file.name.encode('ascii', 'xmlcharrefreplace')
    response['Content-Disposition'] = (u'attachment; filename=\"%s\";' % file.name).encode('utf-8')
    #response['Content-Length'] = u'%d;' % file.file.size
    response.write(open(file.file.path).read())
    return response
