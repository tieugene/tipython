    def	__do_lock(self, request, path):
        '''
        Process LOCK WebDAV request.
        @return: http response:
          - 200	ok,
          - 201	locked new resource,
          - 207	error,
          - 409	no parent,
          - 412	refresh of inexisting lock,
          - 423	locked
        '''
        wdp.util.LOG('LOCK: %s', path)
        resource = self.__ds.get_child(path)
        ret_200 = False
        if ((resource) and (not resource.is_collection())):
            # 0. GET request
            timeout	= request.META.get('HTTP_TIMEOUT', None)
            if timeout:
                timeout = int(timeout.lstrip('Second-'))
            refresh	= request.META.get('HTTP_IF', None)
            if (not refresh):
                print type(resource)
                __lock = resource.set_lock(timeout)
                if (__lock):
                    token, timeout = __lock
                    ret_200 = True
                else:
                    return wdp.hr.http_423('bad request')	# FIXME: add body
            else:
                token = refresh.split(':', 1)[1][:32]		# FIXME: It's a locker problem
                timeout = resource.re_lock(token, timeout)
                if (timeout):
                    ret_200 = True
        if (ret_200):
            etree.register_namespace('D', 'DAV:')
            root = etree.Element('{DAV:}prop')
            activelock = etree.SubElement(etree.SubElement(root, '{DAV:}lockdiscovery'), '{DAV:}activelock')
            etree.SubElement(etree.SubElement(activelock, '{DAV:}locktype'), '{DAV:}write')
            etree.SubElement(etree.SubElement(activelock, '{DAV:}lockscope'), '{DAV:}exclusive')
            etree.SubElement(activelock, '{DAV:}depth').text = '0'
            etree.SubElement(activelock, '{DAV:}timeout').text = 'Second-%d' % timeout
            etree.SubElement(etree.SubElement(activelock, '{DAV:}locktoken'), '{DAV:}href').text = 'opaquelocktoken:' + token
            content = etree.tostring(root, pretty_print=False, encoding='utf-8', xml_declaration=True)
            return wdp.hr.http_200(
                content = content,
                content_type = wdp.const.MIME_XML,
                head = {'Lock-Token': '<opaquelocktoken:%s>' % token} if (refresh) else {},
            )
        return wdp.hr.http_404()

    def	__do_unlock(self, request, path):
        '''
        Process UNLOCK WebDAV request.
        @return: http response:
          - 204	ok,
          - 400	no token,
          - 403	not permitted,
          - 404?	not found,
          - 409	not locked
        '''
        wdp.util.LOG('UNLOCK: %s', path)
        resource = self.__ds.get_child(path)
        if (resource):
            token = request.META.get('HTTP_LOCK_TOKEN', None)
            if (token):
                token = token.split(':', 1)[1][:32]		# FIXME:
                if (resource.un_lock(token)):
                    return wdp.hr.http_204()
        return wdp.hr.http_404()
