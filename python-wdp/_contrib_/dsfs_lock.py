    def	set_lock(self, timeout = None):
        ''''''
        #wdp.util.LOG('dsfs.lock')
        if (self._locker):
            #wdp.util.LOG('try lock')
            return self._locker.set(self._path, timeout)

    def	get_lock(self):
        ''''''
        #wdp.util.LOG('dsfs.getlock')
        if (self._locker):
            #wdp.util.LOG('try lock')
            return self._locker.get(self._path)

    def	re_lock(self, token, timeout = None):
        ''''''
        #wdp.util.LOG('dsfs.relock')
        if (self._locker):
            return self._locker.reset(self._path, token, timeout)

    def	un_lock(self, token):
        ''''''
        #wdp.util.LOG('dsfs.unlock')
        if (self._locker):
            return self._locker.delete(self._path, token)
