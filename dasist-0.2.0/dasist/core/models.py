"""Core.models"""

# 1. system
import os
import hashlib
import uuid
import logging
# 2. django
from django.conf import settings
# from django.core.files.base import ContentFile
from django.db import models, transaction
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
# from django.utils.translation import gettext as _
# 3. 3rd parties
import magic
# 4. local
# const
FILE_MASK = '%08d'
# var
logger = logging.getLogger(__name__)


def my_upload_to(instance, filename: str) -> str:
    """Generates upload path for FileField
    :param instance: ...
    :param filename: ...
    """
    instance.name = filename
    return "temp/%s" % uuid.uuid4().hex.upper()


class File(models.Model):
    """Elementary file storage item"""
    file = models.FileField(null=False, upload_to=my_upload_to, verbose_name='File')
    name = models.CharField(null=False, blank=False, db_index=True, max_length=255, verbose_name='File name')
    size = models.PositiveIntegerField(null=False, db_index=True, verbose_name='Size')
    ctime = models.DateTimeField(null=False, blank=False, db_index=True, auto_now_add=True, verbose_name='Created')
    mime = models.CharField(null=False, blank=False, db_index=True, max_length=16, verbose_name='Mime time')
    md5 = models.CharField(null=False, blank=False, db_index=True, max_length=32, verbose_name='CRC')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('file_view', kwargs={'pk': self.pk})

    def get_filename(self) -> str:
        """
        :return: Real (on disk) file name
        """
        return FILE_MASK % self.pk

    def get_path(self) -> str:
        """
        :return: Real absolute file path
        """
        return os.path.join(settings.MEDIA_ROOT, self.get_filename())

    @staticmethod
    def file_md5(file, block_size: int = 1024 * 14) -> str:
        """Calculates file md5sum.
        :param file: file name or file object, opened for read.
        :param block_size: size in bytes buffer for calc md5.
        :return: hex representation of MD5
        """
        if isinstance(file, str):
            file = open(file, 'rb')
        h = hashlib.md5()
        block = file.read(block_size)
        while block:
            h.update(block)
            block = file.read(block_size)
        return h.hexdigest()

    def raw_save(self):
        """Save object without pre/post signals.
        For DB import only."""
        super().save()

    def update_meta(self):
        """Update md5 and size to real values."""
        path = self.get_path()
        self.size = os.path.getsize(path)
        self.md5 = self.file_md5(path)
        super().save()

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'


@receiver(pre_save, sender=File)
def _file_pre_save(sender, instance: File, **kwargs):
    """Define name, size, mime, crc
    Mime for django: https://medium.com/@ajrbyers/file-mime-types-in-django-ee9531f3035b
    Uploaded is django.core.files.uploadedfile.InMemoryUploadedFile/TemporaryUploadedFile (small/3MB+)
    """
    def get_file_mime(fobj) -> str:
        """
        :param fobj:
           - new/replace - django.core.files.uploadedfile.InMemoryUploadedFile (for newly created)
           - edit (w/o changing file itself) - django.core.files.base.File
        :return: file mimetype
        :note: https://stackoverflow.com/questions/4853581/django-get-uploaded-file-type-mimetype
        """
        pos = fobj.tell()
        fobj.seek(0)
        mime = magic.detect_from_content(fobj.read(1024)).mime_type
        fobj.seek(pos)
        return mime

    def get_file_crc(f, block_size: int = 1024 * 14) -> str:
        """Calculates file CRC.
        :param f: in admin
           - new/replace - django.core.files.uploadedfile.InMemoryUploadedFile (for newly created)
           - edit (w/o changing file itself) - django.core.files.base.File
        :param block_size: size in bytes buffer for calc md5.
        :return: hex representation of MD5
        """
        pos = f.tell()
        f.seek(0)
        h = hashlib.md5()
        block = f.read(block_size)
        while block:
            h.update(block)
            block = f.read(block_size)
        f.seek(pos)
        # TODO: iterate over file.chunks() if (file.multiple_chunks())
        return h.hexdigest()

    file = instance.file
    if isinstance(file.file, InMemoryUploadedFile) or isinstance(file.file, TemporaryUploadedFile):
        logger.debug(f"Pre-save '{file.name}'")
        instance.name = file.name
        instance.size = file.size
        instance.mime = get_file_mime(file.file)
        instance.md5 = get_file_crc(file.file)


@receiver(post_save, sender=File)
def _file_post_save(sender, instance: File, created: bool, **kwargs):
    """
    Powered by https://dev.retosteffen.ch/2017/09/django-uploading-image-post_save/
    """
    if created:
        file = instance.file
        old_name = file.name
        new_name = instance.get_filename()
        logger.debug(f"Post-save '{old_name}' => '{new_name}'")
        if not old_name:    # ?
            return
        new_path = instance.get_path()
        new_dir = os.path.dirname(new_path)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.rename(file.path, new_path)
        instance.file.name = new_name
        instance.save()


@receiver(post_delete, sender=File)
def _file_delete(sender, instance: File, **kwargs):
    p = instance.get_path()
    if os.path.exists(p):
        os.unlink(p)


class FileSeq(models.Model):
    """File sequence
    :todo: del file
    """
    files = models.ManyToManyField(File, through='FileSeqItem', verbose_name='Files')

    def __str__(self):
        return str(self.pk)

    def clean_children(self):
        """Delete all files in"""
        self.files.all().delete()

    def delete(self, *args, **kwargs):
        """Delete self and all files in"""
        self.clean_children()
        super().delete(*args, **kwargs)

    def add_file(self, f: File):
        """Append new File"""
        FileSeqItem(file=f, fileseq=self, order=self.files.count() + 1).save()

    @transaction.atomic
    def del_file(self, pk):
        fsi = self.fileseqitem_set.get(file=pk)
        order = fsi.order
        fsi.file.delete()
        # self.fileseqitem_set.all().order_by('order').filter(order__gt=ord).update(order=order-1)
        for i in self.fileseqitem_set.all().order_by('order').filter(order__gt=order):
            i.order = i.order - 1
            i.save()

    def list_items(self):
        return self.fileseqitem_set.all().order_by('order')

    class Meta:
        # unique_together        = (('invarch', 'type', 'name'),)
        ordering = ('id',)
        verbose_name = 'File sequence'
        verbose_name_plural = 'File sequences'


@receiver(post_delete, sender=FileSeq)
def _fileseq_delete(sender, instance, **kwargs):
    sender.clean_children(instance)


class FileSeqItem(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE, primary_key=True, verbose_name='File')
    fileseq = models.ForeignKey(FileSeq, on_delete=models.CASCADE, db_index=True, verbose_name='File sequence')
    order = models.PositiveSmallIntegerField(db_index=True, verbose_name='#')

    # def    __unicode__(self):
    #    return '%s: %s' % (self.user, self.comment)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    @transaction.atomic
    def swap(self, sibling: int):
        """Swap two nearby files.
        :param sibling: Item order to swap with
        """
        new_fsi = self.fileseq.fileseqitem_set.get(order=sibling)
        old_order = self.order
        new_order = new_fsi.order
        new_fsi.order = old_order
        new_fsi.save()
        self.order = new_order
        self.save()

    def is_first(self) -> bool:
        return self.order == 1

    def is_last(self) -> bool:
        return self.order == self.fileseq.files.count()

    class Meta:
        ordering = ('file', 'order',)
        verbose_name = 'Sequience file'
        verbose_name_plural = 'Sequence files'
