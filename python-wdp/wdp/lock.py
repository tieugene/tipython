# -*- coding: utf-8 -*-
'''
Locker implementation.
Maybe to made Lock[Entry] as separate class (like DavResource).
@undocumented: __package__
'''

import datetime
import uuid
from wdp.util import LOG

class	Locker:
    '''
    Ready to use Lock/Unlock manager.
    Object of this type is passing to DavStorage to handle locks.
    Deletes timeouted locks on each request.
    Now implemented only:
      - members
      - 1 token per entry
      - exclusive locks
    '''
    def	__init__(self, max_timeout=300):
        '''
        Init locker object.
        @param max_timeout: max timeout
        @type max_timeout: int
        '''
        self.__max_timeout = max_timeout
        self.__data = dict()    # entry: (token:str, due:datetime)

    def __fix_timeout(self, timeout):
        '''
        Fix timeout due max timeout
        @param timeout: timeout
        @type timeout: int
        @return: timeout
        @rtype: int
        '''
        if ((not timeout) or ((timeout) and (timeout > self.__max_timeout))):
            timeout = self.__max_timeout
        return timeout

    @staticmethod
    def __gen_token():
        '''
        Generates new token.
        @return: token
        @rtype: str
        '''
        return uuid.uuid4().hex.upper()

    def get(self, entry):
        '''
        Get lock. If exists and timeout - delete them.
        @param entry: locked entry
        @type entry: any
        @return: (token, timeout)|None
        @rtype: tuple(str, int)|None
        '''
        LOG('lock.get: %s', entry)
        __lock = self.__data.get(entry, None)
        if ((__lock) and (__lock[1] <= datetime.datetime.now())):
            del self.__data[entry]
            __lock = None
        return __lock

    def set(self, entry, timeout=None):
        '''
        Set new lock.
        @param entry: Entry to lock
        @type entry: any
        @param timeout: Desired timeout
        @type timeout: int
        @return: (token, timeout)|None (no locker, lock exists)
        @rtype: tuple(str, int)|None
        '''
        LOG('lock.set: %s', entry)
        __lock = self.get(entry)
        if (__lock):
            return None     # Err: already locked
        timeout = self.__fix_timeout(timeout)
        __lock = (self.__gen_token(), datetime.datetime.now() + datetime.timedelta(0, timeout))
        self.__data[entry] = __lock
        return (__lock[0], timeout)       # Ok: new

    def reset(self, entry, token, timeout=None):
        '''
        Refresh existing lock - if entry and token match.
        @param entry: Entry to refresh
        @param token: Lock token to refresh
        @type token: str
        @param timeout: Desired timeout
        @type timeout: int
        @return: timeout|None (no locker, lock not exists, token mismatch)
        @rtype: int|None
        '''
        LOG('lock.reset: %s', entry)
        __lock = self.get(entry)
        if ((__lock) and (__lock[0] == token)):
            timeout = self.__fix_timeout(timeout)
            self.__data[entry] = (self.__gen_token(), datetime.datetime.now() + datetime.timedelta(0, self.__fix_timeout(timeout)))
            return timeout
        return None

    def delete(self, entry, token):
        '''
        Delete lock - if entry and token match.
        @param entry: Entry which lock to delete
        @param token: Lock to delete
        @type token: str
        @return: success
        @rtype: bool
        '''
        LOG('lock.delete: %s, %s', entry, token)
        __lock = self.get(entry)
        if(__lock):
            if (__lock[0] == token):
                del self.__data[entry]
                return True
        return False
