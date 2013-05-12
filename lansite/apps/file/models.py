# -*- coding: utf-8 -*-
'''
TODO: all of MIME types: audio, image, text, video
(option: application, example, message, model, multipart
'''

# 1. django
from django.db import models

# 2. system
import os, hashlib
from PIL import Image, ImageSequence

# 3. 3rd party
from xdg import Mime

# 4. local
from apps.core.models import *
from rfm import RenameFilesModel
from settings import MEDIA_ROOT, LOGIN_REDIRECT_URL
#from apps.file.views import file_detail

def    my_upload_to(instance, filename):
    '''
    Generates upload path for FileField
    '''
    instance.name = filename
    return u'temp/%s' % filename

def file_md5(file, block_size=1024*14):
    '''
    file_md5(file, use_system = False) -> md5sum of "file" as hexdigest string.
    "file" may be a file name or file object, opened for read.
    If "use_system" is True, if possible use system specific program. This ignore, if file object given.
    "block_size" -- size in bytes buffer for calc md5. Used with "use_system=False".
    '''
    if isinstance(file, basestring):
        file = open(file, 'rb')
    h = hashlib.md5()
    block = file.read(block_size)
    while block:
        h.update(block)
        block = file.read(block_size)
    return h.hexdigest()

class    File(Object, RenameFilesModel):
	'''
	TODO: inherit Object
	WARNING: mkdir -p MEDIA_ROOT/temp; files will be placed into MEDIA_ROOT as ########
	'''
	file        = models.FileField        (null=False, upload_to=my_upload_to, verbose_name=u'Файл')    # attrs: name, path, url, size
	name        = models.CharField        (null=False, blank=False, max_length=255, verbose_name=u'Имя файла')
	mime        = models.CharField        (null=False, blank=False, max_length=255, verbose_name=u'Тип Mime')
	saved       = models.DateTimeField        (null=False, blank=False, auto_now_add=True, verbose_name=u'Записано')
	size        = models.PositiveIntegerField    (null=False, blank=False, verbose_name=u'Размер')
	md5         = models.CharField        (null=False, blank=False, max_length=32, verbose_name=u'MD5')
	RENAME_FILES    = {'file': {'dest': '', 'keep_ext': False}}

	def    save(self):
		'''
		file: <InMemoryUploadedFile: 2.html (text/html)>
		django...file: _get_size
		'''
		self.mime = self.file._file.content_type
		self.size = self.file._file._size
		self.md5 = file_md5(self.file._file.file)
		super(File, self).save()

	def    raw_save(self):
		'''
		For import only
		'''
		super(File, self).save()

	def    __unicode__(self):
		return self.name

	@models.permalink
	def	get_absolute_url(self):
		return ('apps.file.views.file_detail', [str(self.pk)])

	def	get_edit_url(self):
		return ('apps.file.views.file_edit', [str(self.pk)])

	def	get_del_url(self):
		return ('apps.file.views.file_del', [str(self.pk)])

	class    Meta:
		app_label = 'gw'
		verbose_name = u'Файл'
		verbose_name_plural = u'Файлы'

class    ImageFile(File):
	'''
	Mime: image/ (e.g. g3fax, gif, jpeg, png, tiff, tiff-fx)
	? ImageField?
	TODO: h, w, resolution, depth
	TODO: multipage, caching (thumbnails) - 256, 512, screen, full
	'''
	width        = models.PositiveIntegerField    (null=False, blank=False, default=0, verbose_name=u'Ширина')
	height       = models.PositiveIntegerField    (null=False, blank=False, default=0, verbose_name=u'Высота')
	pages        = models.PositiveIntegerField    (null=False, blank=False, default=0, verbose_name=u'Страниц')

	def    save(self):
		im = Image.open(self.file._file.file, 'r')
		if im:
		    size = im.size
		    index = 0
		    for frame in ImageSequence.Iterator(im):
			index = index + 1
		    self.width    = size[0]
		    self.height    = size[1]
		    self.pages    = index
		super(ImageFile, self).save()

	def    raw_save(self):
		'''
		For import only
		'''
		super(ImageFile, self).raw_save()

	def    getthumbs(self, tsize = 512):
		'''
		Get cached resized image
		@tsize - max size
		@return list of cached thumbnails
		TODO: preview (bmp?, gif, ?ico, jpg, png) or tiff=>gif/jpg/png (1-bit, max 512)
		Maybe - inline images?
		Or - tmp file cache like "id.page" (+size, bits)
		---
		So, thumb filename: cache.img/<filename>_<page>[_size].<ext>
		TODO: check files befor handle picture
		'''
		retvalue = list()
		name = self.getfilename()
		ext = self.mime.split('/',1)[1]
		if ext == 'tiff':
		    ext = 'png'
		im = Image.open(MEDIA_ROOT+'/' + self.getfilename(), 'r')
		if im:
		    size = im.size
		    if (max(size[0], size[1]) <= tsize):
			toresize = False
			dfilename = 'cache.img/%s_%%d.%s' % (name, ext)
		    else:
			toresize = True
			dfilename = 'cache.img/%s_%%d_%d.%s' % (name, tsize, ext)
		    # let's go
		    index = 0
		    for frame in ImageSequence.Iterator(im):
			tmpfilename = dfilename % index
			dfile = MEDIA_ROOT+'/' + tmpfilename
			if not os.path.exists(dfile):
			    if (toresize):
				frame.thumbnail((tsize, tsize))
			    frame.save(dfile)
			index = index + 1
			retvalue.append(tmpfilename)
		return retvalue

	class    Meta:
		app_label = 'gw'
		verbose_name = u'Изображение'
		verbose_name_plural = u'Изображения'
