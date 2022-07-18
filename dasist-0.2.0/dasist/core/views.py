# -*- coding: utf-8 -*-
"""
core.views
"""

# 1. system
import json
# 2. 3rd parties
from dal import autocomplete
# 3. django
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
# from django.db import transaction
# 4. my
from . import models, forms

PAGE_SIZE = 25


class FileList(ListView):
    model = models.File
    template_name = 'core/file_list.html'
    paginate_by = PAGE_SIZE


class FileDetail(DetailView):
    model = models.File
    template_name = 'core/file_view.html'


class FileSeqList(ListView):
    model = models.FileSeq
    template_name = 'core/fileseq_list.html'
    paginate_by = PAGE_SIZE


class FileSeqDetail(DetailView):
    model = models.FileSeq
    template_name = 'core/fileseq_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FileSeqDetail, self).get_context_data(**kwargs)
        context['form'] = forms.FileSeqItemAddForm()
        return context


@login_required
def file_preview(request, pk):
    return render(request, 'core/file_img.html', {'file': models.File.objects.get(pk=int(pk))})


@login_required
def file_get(request, pk):
    """
    Download file
    """
    file = models.File.objects.get(pk=int(pk))
    response = HttpResponse(content_type=file.mime)
    response['Content-Transfer-Encoding'] = 'binary'
    response['Content-Disposition'] = '; filename=\"%s\"' % file.name.encode('utf-8')
    response.write(open(file.get_path()).read())
    return response


@login_required
def file_del(request, pk):
    models.File.objects.get(pk=int(pk)).delete()
    return redirect('file_list')


@login_required
def fileseq_add_file(request, pk):
    form = forms.FileSeqItemAddForm(request.POST, request.FILES)
    if form.is_valid():
        if 'file' in request.FILES:
            fileseq = models.FileSeq.objects.get(pk=int(pk))
            file = models.File(file=request.FILES['file'])
            file.save()
            fileseq.add_file(file)
    return redirect('fileseq_view', pk)


@login_required
def fileseq_del(request, pk):
    models.FileSeq.objects.get(pk=int(pk)).delete()
    return redirect('fileseq_list')


@login_required
def fileseqitem_del(request, pk):
    fsi = models.FileSeqItem.objects.get(pk=int(pk))
    fs = fsi.fileseq
    fs.del_file(int(pk))
    return redirect('fileseq_view', fs.pk)


@login_required
def fileseqitem_move_up(request, pk):
    fsi = models.FileSeqItem.objects.get(pk=int(pk))
    fs = fsi.fileseq
    order = fsi.order
    if order > 1:
        fsi.swap(fsi.order - 1)
    return redirect('fileseq_view', fs.pk)


@login_required
def fileseqitem_move_down(request, pk):
    fsi = models.FileSeqItem.objects.get(pk=int(pk))
    fs = fsi.fileseq
    order = fsi.order
    if fs.files.count() > order:
        fsi.swap(fsi.order + 1)
    return redirect('fileseq_view', fs.pk)
