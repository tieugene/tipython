# -*- coding: utf-8 -*-
'''
DavStorage - pure virtual (except Resource constructor and is_collection()) and for documenting class.
Each method returns something (on success) or None (on error).
You MUST to inherit this classes into your implementation - as last parent.
@undocumented: __package__
'''

import sys
import wdp.util

reload(sys)
sys.setdefaultencoding('utf-8')

class	Resource(object):
    ''' Common dav resource things '''

    __premask = '%s.Resource.%%s: %%s' % __name__

    def	__init__(self, path, locker=None):
        '''
        @param path: resource id
        @type path: str
        @param locker: locker
        @type locker: Locker
        '''
        self._path = path
        self._locker = locker

    def _log(self, funcname, mask, *args):
        '''
        Log.
        TODO: loglevel
        @param funcname: name of caller
        @type funcname: str
        @param mask: mask to print
        @type mask: str
        '''
        wdp.util.LOG(self.__premask % (funcname, mask), *args)

    def	get_options(self):
        '''
        WebDAV OPTIONS supportable with the resource.
        Callers: OPTIONS etc.
        @return: options
        @rtype: int
        '''
        self._log('get_options', '"%s"', self._path)
        return 0

    def	get_ctime(self):
        '''
        Get resource creation time.
        Callers: PROPFIND.
        @return: Creation date and time
        @rtype: datetime
        '''
        self._log('get_ctime', '"%s"', self._path)

    def	get_mtime(self):
        '''
        Get resource last modification time.
        Callers: PROPFIND.
        @return: Last modification date and time
        @rtype: datetime
        '''
        self._log('get_mtime', '"%s"', self._path)

    def	delete(self):
        '''
        Delete resource [recursively].
        Callers: DELETE.
        @return: success
        @rtype: bool
        '''
        self._log('delete', '"%s"', self._path)

    def	_cp_to(self, dstpath):
        '''
        Copy resource to dst.
        Inner method.
        @param dstpath: destination
        @type dstpath: str
        @return: success
        @rtype: bool
        '''
        self._log('_cp_to', '"%s"=>"%s"', self._path, dstpath)

    def	_mv_to(self, dstpath):
        '''
        Move resource from self to path
        Inner method.
        @param dstpath: destination
        @type dstpath: str
        @return: success
        @rtype: bool
        '''
        self._log('_mv_to', '"%s"=>"%s"', self._path, dstpath)

class	Member(Resource):
    '''
    Member specific things.
    '''
    __premask = '%s.Member.%%s: %%s' % __name__

    @staticmethod
    def	is_collection():
        '''
        Check resource is collection.
        Callers: all.
        @return: False
        @rtype: bool
        '''
        return False

    def	get_size(self):
        '''
        Get member size.
        Callers: PROPFIND.
        @return: member size
        @rtype: int
        '''
        self._log('get_size', '"%s"', self._path)

    def	get_mime(self):
        '''
        Get member mime type.
        Callers: PROPFIND.
        @return: member mime type
        @rtype: str
        '''
        self._log('get_mime', '"%s"', self._path)

    def	read(self, start=0L, size=0L):
        '''
        Read member content.
        Callers: GET.
        @param start: lseek
        @type start: long
        @param size: read block size
        @type start: long
        @return: member content
        '''
        self._log('read', '"%s" (from %d, %d bytes)', self._path, start, size)

    def	write(self, data):
        '''
        Rewrite member content.
        Callers: PUT (exists).
        @return: success
        @rtype: bool
        '''
        self._log('write', '"%s" (%d)', self._path, len(data))

    def	set_lock(self, timeout=None):
        '''
        Lock member.
        Callers: LOCK (new).
        @param timeout: timeout desired
        @type timeout: int
        @return:
          - token
          - timeout
        @rtype: tuple(str, int)
        '''
        self._log('set_lock', '"%s" (for %d seconds)', self._path, int(timeout))

    def	get_lock(self):
        '''
        Get member lock[s].
        Callers: all.
        @return:
          - token
          - timeout
        @rtype: tuple(str, int)
        '''
        self._log('get_lock', '"%s"', self._path)

    def	re_lock(self, token, timeout=None):
        '''
        ReLock member.
        Callers: LOCK (refresh).
        @param timeout: in seconds
        @type timeout: int
        @param token: token
        @type token: str
        @return: timeout
        @rtype: int
        '''
        self._log('re_lock', '"%s" (by %s on %d seconds)', self._path, token, int(timeout))

    def	un_lock(self, token):
        '''
        UnLock member.
        Callers: UNLOCK.
        @param token: token
        @type token: str
        @return: success
        @rtype: bool
        '''
        self._log('un_lock', '"%s" (by %s)', self._path, token)

class	Collection(Resource):
    ''' Collection specific things '''

    __premask = '%s.Collection.%%s: %%s' % __name__

    @staticmethod
    def	is_collection():
        '''
        Check resource is collection.
        Callers: all.
        @return: True
        @rtype: bool
        '''
        return True

    def	get_children(self):
        '''
        Get collection members.
        Callers: PROPFIND.
        @return: children resources
        @rtype: list
        '''
        self._log('get_children', '"%s"', self._path)

    def	get_child(self, uritail):
        '''
        Get collection member.
        Callers: all.
        @param uritail: resource relative location
        @type uritail: str
        @return: member|collection object
        @rtype: Member|Collection
        '''
        self._log('get_child', '"%s" => "%s"', self._path, uritail)

    def	mk_col(self, uritail):
        '''
        Create new collection.
        Callers: MKCOL.
        @param uritail: resource relative location
        @type uritail: str
        @return: collection object
        @rtype: Collection
        '''
        self._log('mk_col', '"%s" => "%s"', self._path, uritail)

    def	mk_mem(self, uritail, data):
        '''
        Create new member.
        Callers: PUT (new).
        @param uritail: resource relative location
        @type uritail: str
        @param data: content
        @return: member object
        @rtype: Member
        '''
        self._log('mk_mem', '"%s" => "%s" (%d bytes)', self._path, uritail, len(data))

class	Storage(Collection):
    '''
    Storage root.
    Passed to DavProvider as "callback" to handle real data.
    '''
    def	move(self, src, dstpath):
        '''
        Move one resource to another.
        Callers: MOVE.
        @param src: source resource
        @type src: Resource
        @param dst: destination path tail
        @type dst: str
        @return: success
        @rtype: bool
        '''
        self._log('copy', '"%s" => "%s"', src._path, dstpath)

    def	copy(self, src, dstpath):
        '''
        Copy one resource to another.
        Callers: COPY.
        @param src: source resource
        @type src: Resource
        @param dst: relative destination path tail
        @type dst: str
        @return: success
        @rtype: bool
        '''
        self._log('move', '"%s" => "%s"', src._path, dstpath)
