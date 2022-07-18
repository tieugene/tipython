# -*- coding: utf-8 -*-
'''
DavStorage FileSystem implementation.
Dox:
* http://www.doughellmann.com/articles/how-tos/python-exception-handling/index.html
* http://docs.python.org/tutorial/errors.html
TODO: try..except for file operations:
* _MIME.file()
* open()    IOError
* file.read()   ?
* file.write(x2)    ?
* file.close()  ValueError
* file.flush()  ?
* os.stat() OSError?
* os.remove()   OSError? (.args = (.errno, .strerror))
* os.listdir()  OSError?
* os.mkdir()  OSError?
* os.path.exists()
* os.path.isdir()
* shutil.copy2()
* shutil.rmtree()
* shutil.copytree()
TODO: retvalue => error, retvalue (error = (const.DS_*, uritail, errstring))
TODO: log exceptions (sys.exc_info(): (type:class, value, traceback:traceback)) - exname, errcode, errstring, abspath, funcname, stringno, uritail
@undocumented: __package__
'''
# 1. system
import os
import sys
import datetime
import shutil

# 2. 3rd parties
import magic

# 3. my
#from ds import DavStorageMember, DavStorageCollection
import wdp.ds
import wdp.util
import wdp.const

# 4. consts
reload(sys)
sys.setdefaultencoding('utf-8')

_MIME = magic.open(magic.MIME_TYPE)    # mime DB
_MIME.load()
_OPT_MEMBER = wdp.const.OPT_GET | wdp.const.OPT_PUT | wdp.const.OPT_DELETE | wdp.const.OPT_PROPFIND | wdp.const.OPT_COPY | wdp.const.OPT_MOVE
_OPT_COLLECTION = wdp.const.OPT_DELETE | wdp.const.OPT_PROPFIND | wdp.const.OPT_MKCOL | wdp.const.OPT_COPY | wdp.const.OPT_MOVE
_OPT_STORAGE = _OPT_MEMBER | _OPT_COLLECTION

class	FSResource(wdp.ds.Resource):
    ''' Common things for folders/files '''

    __premask = '%s.FSResource.%%s: %%s' % __name__

    def	__init__(self, path, locker=None):
        '''
        @param path: absolute resource path
        @type path: str
        '''
        self._stat = None
        super(FSResource, self).__init__(path, locker)

    def	_try_stat(self):
        ''' Cache stat info '''
        if (not self._stat):
            self._stat = os.stat(self._path.encode('utf-8'))

    def	get_ctime(self):
        ''''''
        self._try_stat()
        return datetime.datetime.fromtimestamp(self._stat.st_ctime)

    def	get_mtime(self):
        ''''''
        self._try_stat()
        return datetime.datetime.fromtimestamp(self._stat.st_mtime)

    def	_mv_to(self, dstpath):
        '''
        @param dst: absolute dest path
        '''
        #wdp.util.LOG('dsfs.mv_to: %s > %s', self._path, dst)
        retvalue = False
        try:
            shutil.move(self._path.encode('utf-8'), dstpath.encode('utf-8'))
            self._path = dstpath
            self._stat = None
            retvalue = True
        except:
            pass
        return retvalue

class	FSMember(FSResource, wdp.ds.Member):
    ''' File things '''

    __premask = '%s.FSMember.%%s: %%s' % __name__

    def	get_options(self):
        return _OPT_MEMBER

    def	get_size(self):
        ''''''
        self._try_stat()
        return self._stat.st_size

    def	get_mime(self):
        ''''''
        return _MIME.file(self._path.encode('utf-8'))

    def	read(self, start=0L, size=0L):
        ''''''
        #wdp.util.LOG('dsfs.read: %s', self._path)
        tmpf = open(self._path.encode('utf-8'), 'r')
        tmpf.seek(start)
        return tmpf.read(size) if (size) else tmpf.read()

    def	write(self, data):
        ''''''
        #wdp.util.LOG('dsfs.write: %s', self._path)
        try:
            __file = open(self._path.encode('utf-8'), 'w')
            __file.write(data)
            __file.flush()  # FIXME: Note: flush() does not necessarily write the file’s data to disk. Use flush() followed by os.fsync() to ensure this behavior.
            #os.fsync()
            __file.close()
            self._stat = None
            retvalue = True
        except:
            retvalue = False
        return retvalue

    def	delete(self):
        ''''''
        #wdp.util.LOG('dsfs.m.del: %s', self._path)
        retvalue = False
        try:
            os.remove(self._path.encode('utf-8'))
            retvalue = True
        except:
            pass
        return retvalue

    def	_cp_to(self, dstpath):
        '''
        @param dst: absolute dest path
        '''
        #wdp.util.LOG('dsfs.m.cp_to: %s > %s', self._path, dstpath)
        retvalue = False
        try:
            shutil.copy2(self._path.encode('utf-8'), dstpath.encode('utf-8'))   # FIXME: absolute
            retvalue = True
        except:
            pass
        return retvalue

class	FSCollection(FSResource, wdp.ds.Collection):
    ''' Folder things. '''

    __premask = '%s.FSCollection.%%s: %%s' % __name__

    def	get_options(self):
        return _OPT_COLLECTION

    def	get_children(self):
        ''''''
        #wdp.util.LOG('dsfs.list: %s', self._path)
        return os.listdir(self._path.encode('utf-8'))

    def	get_child(self, uritail):
        '''
        @rtype: FSCollection/FSMember|None
        '''
        #wdp.util.LOG('dsfs.child: %s > %s', self._path, uritail)
        if (not uritail):
            return self
        __path = os.path.join(self._path, uritail)
        if (os.path.exists(__path.encode('utf-8'))):
            if (os.path.isdir(__path.encode('utf-8'))):
                return FSCollection(__path, self._locker)
            else:
                return FSMember(__path, self._locker)

    def	delete(self):
        ''''''
        #wdp.util.LOG('dsfs.c.del: %s', self._path)
        retvalue = False
        try:
            shutil.rmtree(self._path.encode('utf-8'))
            retvalue = True
        except:
            pass
        return retvalue

    def	_cp_to(self, dstpath):
        '''
        @param dst: absolute path of dest
        '''
        #wdp.util.LOG('dsfs.c.cp_to: %s > %s', self._path, dst)
        retvalue = False
        try:
            shutil.copytree(self._path.encode('utf-8'), dstpath.encode('utf-8'))
            retvalue = True
        except:
            pass
        return retvalue

    def	mk_mem(self, uritail, data):
        '''
        @rtype: FSMember|None
        '''
        #wdp.util.LOG('dsfs.mk_mem: %s', uritail)
        __path = os.path.join(self._path, uritail)
        #wdp.util.LOG('dsfs.mk_mem: %s', __path)
        try:
            __file = open(__path.encode('utf-8'), 'w')
            __file.write(data)
            __file.flush()
            __file.close()
            __retvalue = FSMember(__path, self._locker)
        except:
            __retvalue = None
        return __retvalue

    def	mk_col(self, uritail):
        '''
        @rtype: FSCollection|None
        '''
        #self._log('mk_col', '"%s"', uritail)
        retvalue = None
        __path = os.path.join(self._path, uritail)
        try:
            os.mkdir(__path.encode('utf-8'))
            retvalue = FSCollection(__path, self._locker)
        except:
            pass
        return retvalue

class	FSStorage(FSCollection, wdp.ds.Storage):
    ''' Root '''

    def	get_options(self):
        return _OPT_STORAGE

    def	copy(self, src, dstpath):
        ''''''
        #wdp.util.LOG('dsfs.copy: %s > %s', src, dstpath)
        return src._cp_to(os.path.join(self._path, dstpath))

    def	move(self, src, dstpath):
        ''''''
        #wdp.util.LOG('dsfs.move: %s > %s', src, dstpath)
        return src._mv_to(os.path.join(self._path, dstpath))
