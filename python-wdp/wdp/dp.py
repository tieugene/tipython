# -*- coding: utf-8 -*-
'''
DavProvider - middleware to provide http server with right (rfc4918 compatible)
@undocumented: __package__
'''
# 1. system
import os
import sys
#import pprint
import urllib
import re

# 2. 3rd parties
from lxml import etree

# 3. my
import wdp.hr
import wdp.const
import wdp.util

# 5. consts
# utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

RANGE = re.compile('^bytes=(\d*)-(\d*)$')

_OPT_DICT = {
    wdp.const.OPT_GET:          'GET',
    wdp.const.OPT_HEAD:         'HEAD',
    wdp.const.OPT_POST:         'POST',
    wdp.const.OPT_PUT:          'PUT',
    wdp.const.OPT_DELETE:       'DELETE',
    wdp.const.OPT_TRACE:        'TRACE',
    wdp.const.OPT_CONNECT:      'CONNECT',
    wdp.const.OPT_PROPFIND:     'PROPFIND',
    wdp.const.OPT_PROPPATCH:    'PROPPATCH',
    wdp.const.OPT_MKCOL:        'MKCOL',
    wdp.const.OPT_COPY:         'COPY',
    wdp.const.OPT_MOVE:         'MOVE',
}

class	DavProvider:
    '''
    WebDAV provider - provide http WebDAV requests handling.
    '''

    __premask = '%s.DavProvider.%%s: %%s' % __name__

    def	__init__(self, datastorage):
        '''
        Create new DavProvider object.
        @param datastorage: data provider
        @type datastorage: DavStorage
        '''
        self.__func = {
        #	type		function	            standard, mandatory
            'OPTIONS':	self.__do_options,		# HTTP	+
            'PROPFIND':	self.__do_propfind,		# DAV	+
            'GET':		self.__do_get,		    # HTTP	+
            'PUT':		self.__do_put,		    # HTTP	+
            'DELETE':	self.__do_delete,		# HTTP	+
            'MKCOL':	self.__do_mkcol,		# DAV	+
            'COPY':		self.__do_copy,		    # DAV	+
            'MOVE':		self.__do_move,		    # DAV	+
        }
        self.__ds = datastorage
        self.__allowed = self.__get_allowed(self.__ds)

    def __log(self, funcname, mask, *args):
        '''
        Log.
        TODO: loglevel
        @param funcname: name of caller
        @type funcname: str
        @param mask: mask to print
        @type mask: str
        '''
        wdp.util.LOG(self.__premask % (funcname, mask), *args)

    def __get_allowed(self, resource):
        '''
        Get allowed options.
        @param resource: object
        @type resource: wdp.ds.Resource
        @return: options list
        @rtype: str
        '''
        allowed = 'OPTIONS'
        opts = resource.get_options()
        for key, value in _OPT_DICT.iteritems():
            if (opts & key):
                allowed += (',' + value)
        return allowed

    def dispatch(self, request, path):
        '''
        Dispatch inbound http requests to corresponding handlers.
        Path examples: http://www.example.com/dav/collection1/ = > collection1/; root = "".
        All handlers have same params.
        @param request: http request
        @type request: HttpRequest
        @param path: uri substring
        @type path: str
        @rtype: ?
        @return: http response
        '''
        __name = 'Dispatch'
        self.__log(__name, '%s: "%s"', request.method, path)
        if (request.method in self.__func):
            return self.__func[request.method](request, path.rstrip('/'))
        else:
            return wdp.hr.http_405(self.__allowed)

    def	__do_options(self, request, path):
        '''
        Process OPTIONS HTTP request.
        TODO: get options according to self.__ds(path)
        @return: http response:
        * 403 - access denied
        * 200 - other
        '''
        #wdp.util.LOG('%s.%s.options: "%s"', __name__, self.__class__.__name__, path)
        __name = 'OPTIONS'
        self.__log(__name, '"%s"', path)
        if (path):
            resource = self.__ds.get_child(path)
            if (resource):
                allowed = self.__get_allowed(resource)
            else:
                allowed = None
        else:   # cached root options
            allowed = self.__allowed
        if (allowed):
            return wdp.hr.http_200(
                content_type=wdp.const.MIME_FOLDER,
                head={
                    'Allow':		    allowed,
                    'DAV':			    '1',        # was 1,2,<http://apache.org/dav/propset/fs/1>
                    #'MS-Author-Via':	'DAV',
                }
            )
        else:
            return wdp.hr.http_404(path)

    @staticmethod
    def __handle_range_helper(range_str, size):
        '''
        Process Range header.
        If (first > last) => None
        @param range_str: range string
        @type range_str: str
        @param size: file size
        @type size: int
        @return: start, size
        @rtype: tuple|None
        '''
        if (range_str):
            matches = RANGE.match(range_str)
            if (matches):
                if (matches.group(1) == ''):    # suffix-byte-range-spec
                    rsize = min(long(matches.group(2)), size)
                    return (size - rsize, rsize)
                elif (matches.group(2) == ''):  # first only
                    first = long(matches.group(1))
                    return (first, size - first)
                else:                   # first..last
                    first = long(matches.group(1))
                    if (first >= size):
                        return (first, first)
                    else:
                        last = min(long(matches.group(2)), size - 1)
                        if (first <= last):
                            return (first, last - first + 1)

    def	__do_get(self, request, path):
        '''
        Process GET HTTP request.
        Range:
        * if first > last => ignore Range (200)
        * if (last > size) | (last = None) => last == size (206)
        * if -last > size => -last == size (206)
        * if first > size => (416)
        @return: http response:
          - 200 - ok (^Range or (Range and (first > last)))
          - 206 - ok with Range (Content-Range: bytes start-end/size
          - 403 - access denied
          - 404 - not found
          - 416 - Range & (first > size)
        '''

        __name = 'GET'
        self.__log(__name, '"%s"', path)
        resource = self.__ds.get_child(path)
        if (resource):
            if (not resource.is_collection()):
                size = resource.get_size()
                http_range = self.__handle_range_helper(request.META.get('HTTP_RANGE', None), size)
                if (http_range):
                    if (http_range[0] >= size):
                        self.__log(__name, '416 (out of size)')
                        return wdp.hr.http_416()
                    else:
                        self.__log(__name, '206 (partial get)')
                        return wdp.hr.http_206(
                            content=resource.read(http_range[0], http_range[1]),
                            content_type=resource.get_mime(),
                            head={
                                'Last-Modified':	resource.get_mtime().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                                'Accept-Ranges':	'bytes',
                                'Content-Range':	'bytes %d-%d/%d' % (http_range[0], http_range[0] + http_range[1] - 1, size),
                            }
                        )
                else:
                    self.__log(__name, '200 (ok)')
                    return wdp.hr.http_200(
                        content=resource.read(),
                        content_type=resource.get_mime(),
                        head={
                            'Last-Modified':	resource.get_mtime().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                            'Accept-Ranges':	'bytes',
                        }
                    )
            else:
                self.__log(__name, '204 (collection)')
                return wdp.hr.http_204()
        self.__log(__name, '404 (Not found)')
        return wdp.hr.http_404(path)

    def	__do_put(self, request, path):
        '''
        Process PUT HTTP request.
        @return: http response:
          - 201 - created       +
          - 204 - wrote ok      +
          - 405 - collection    +
          - 409 - no parent     +
          - ??? - access denied (precondition error? 401?)
        '''
        #wdp.util.LOG('%s.%s.put: "%s"', __name__, self.__class__.__name__, path)
        __name = 'PUT'
        self.__log(__name, '"%s"', path)
        resource = self.__ds.get_child(path)
        if (resource):  # exists
            if (resource.is_collection()):
                self.__log(__name, '405 (collection)')
                return wdp.hr.http_405(self.__get_allowed(resource))
            if (resource.write(request.read())):
                self.__log(__name, '204 (updated)')
                return wdp.hr.http_204()
        else:
            parent = self.__ds.get_child(os.path.dirname(path))
            if ((not parent) or (not parent.is_collection())):
                self.__log(__name, '409 (parent not exists|collection)')
                return wdp.hr.http_409()
            else:
                resource = parent.mk_mem(os.path.basename(path), request.read())
                if (resource):
                    self.__log(__name, '201 (created)')
                    return wdp.hr.http_201(request.build_absolute_uri())
                else:
                    self.__log(__name, '403 (failed)')
                    return wdp.hr.http_403()    # ?
        self.__log(__name, 'unknown error')

    def	__do_delete(self, request, path):
        '''
        Process DELETE HTTP request.
        @return: http response:
          - 200 - ok (w/ comments)
          - 202 - in progress (todo)
          - 204 - ok
          - 207 - failed
          - 404 - not found
        '''
        #wdp.util.LOG('%s.%s.delete: "%s"', __name__, self.__class__.__name__, path)
        __name = 'DELETE'
        self.__log(__name, '"%s"', path)
        resource = self.__ds.get_child(path)
        if (resource):
            if (resource.delete()):
                self.__log(__name, '204 (ok)')
                return wdp.hr.http_204()
            else:
                self.__log(__name, '401 (Access denied)')   # dummy
                return wdp.hr.http_401()
        self.__log(__name, '404 (not found)')
        return wdp.hr.http_404()

    @staticmethod
    def	__fill_prop_helper(multistatus, props, resource, href):
        '''
        Helper function to fill response for each propfinded resource.
        @param multistatus:etree.Element - point to insert props to
        @param props:set - props to populate
        @param resource:DavResource - resource to fill props about
        @param href:str - relative http uri of resource
        '''
        #print '__fill_prop:', href, (resource)
        iscollection = resource.is_collection()
        if (not props):
            props = set((   # collection
                '{DAV:}creationdate',
                '{DAV:}getlastmodified',
                '{DAV:}getcontenttype',
                '{DAV:}resourcetype',
                '{DAV:}supportedlock',
                '{DAV:}lockdiscovery',
            ))
            if (not iscollection):  # file
                props.update((
                    '{DAV:}getcontentlength',
                ))
        # 2.1. for each responsed
        response = etree.SubElement(multistatus, '{DAV:}response')
        etree.SubElement(response, '{DAV:}href').text = urllib.quote(href.encode('utf-8'))
        #print 'Href: "%s"' % request.get_full_path()
        # 2.1.1. usable values
        propstat = etree.SubElement(response, '{DAV:}propstat')
        etree.SubElement(propstat, '{DAV:}status').text = 'HTTP/1.1 200 OK'
        prop = etree.SubElement(propstat, '{DAV:}prop')
        # 2.1.1.1. fill props
        # 1: inplace
        if ('{DAV:}resourcetype' in props):
            if (iscollection):
                etree.SubElement(etree.SubElement(prop, '{DAV:}resourcetype'), '{DAV:}collection')
            else:
                etree.SubElement(prop, '{DAV:}resourcetype')
            props.remove('{DAV:}resourcetype')
        # 2: inplace
        if ('{DAV:}supportedlock' in props):
            etree.SubElement(prop, '{DAV:}supportedlock')
            props.remove('{DAV:}supportedlock')
        # 3: inplace
        if ('{DAV:}lockdiscovery' in props):
            etree.SubElement(prop, '{DAV:}lockdiscovery')
            props.remove('{DAV:}lockdiscovery')
        # 4: semi-inplace
        if ('{DAV:}getcontenttype' in props):
            etree.SubElement(prop, '{DAV:}getcontenttype').text = 'httpd/unix-directory' if (iscollection) else resource.get_mime()
            props.remove('{DAV:}getcontenttype')
        # 5: semi-inplace
        if ('{DAV:}getcontentlength' in props) and (not iscollection):
            etree.SubElement(prop, '{DAV:}getcontentlength').text = str(resource.get_size())
            props.remove('{DAV:}getcontentlength')
        # 6: call only
        if ('{DAV:}creationdate' in props):
            etree.SubElement(prop, '{DAV:}creationdate').text = resource.get_ctime().strftime('%Y-%m-%dT%H:%M:%SZ')
            props.remove('{DAV:}creationdate')
        # 7: call only
        if ('{DAV:}getlastmodified' in props):
            etree.SubElement(prop, '{DAV:}getlastmodified').text = resource.get_mtime().strftime('%a, %d %b %Y %X GMT')
            props.remove('{DAV:}getlastmodified')
        # 2.1.2. unusables add 404
        if (props):
            propstat = etree.SubElement(response, '{DAV:}propstat')
            etree.SubElement(propstat, '{DAV:}status').text = 'HTTP/1.1 404 Not Found'
            prop = etree.SubElement(propstat, '{DAV:}prop')
            for i in props:
                etree.SubElement(prop, i)

    def	__do_propfind(self, request, path):
        '''
        Process PROPFIND WebDAV request.
        @return: HTTP response:
          - 207 - ok,
          - 403 - Depth=infinite,
          - 404 - Not found
        '''
        #wdp.util.LOG('%s.%s.propfind: "%s"', __name__, self.__class__.__name__, path)
        __name = 'PROPFIND'
        self.__log(__name, '"%s"', path)
        depth = request.META.get('HTTP_DEPTH', None)
        resource = self.__ds.get_child(path)
        if (resource):  # found
            # 0. prepare: props, response
            props = set()
            body = request.read()
            if (len(body)):
                dom = etree.fromstring(body)
                ##wdp.util.LOG('PROPFIND request:')
                ##wdp.util.LOG(wdp.util.pprintxml(dom))
                for i in list(list(dom)[0]):    # lxml.etree._Element (base=None, nsmap={'D': 'DAV:'}, prefix='D', tag='{DAV:}tagname'
                    props.add(i.tag)
            etree.register_namespace('D', 'DAV:')
            multistatus = etree.Element('{DAV:}multistatus')
            # 1. root
            root_href = request.get_full_path()
            self.__fill_prop_helper(multistatus, props.copy(), resource, root_href)
            # 2. process deps
            if ((depth == '1') and (resource.is_collection())):
                for child in resource.get_children():
                    href = os.path.join(root_href, child)
                    member = resource.get_child(child)
                    if (member):
                        if (member.is_collection()):
                            href += '/'
                        self.__fill_prop_helper(multistatus, props.copy(), member, href)
            # 3. flush
            ##wdp.util.LOG('PROPFIND response:')
            ##wdp.util.LOG(wdp.util.pprintxml(multistatus))
            return wdp.hr.http_207(etree.tostring(multistatus, pretty_print=False, encoding='utf-8', xml_declaration=True))
        else:
            self.__log(__name, '404 (not found)')
            return wdp.hr.http_404(path)

    def	__do_mkcol(self, request, path):
        '''
        Process MKCOL WebDAV request.
        @return: http response:
          - 201	+ ok (created)
          - 403	+ can't (access denied etc)
          - 405	+ resource exists
          - 409	+ parent not exists
          - 415	+ body exists
          - 507	- No space (todo)
        '''
        __name = 'MKCOL'
        self.__log(__name, '"%s"', path)
        if (request.body):
            self.__log(__name, '415 (body exists)')
            return wdp.hr.http_415()
        resource = self.__ds.get_child(path)
        if (resource):
            self.__log(__name, '405 (resource exists)')
            return wdp.hr.http_405(self.__get_allowed(resource))
        else:
            parent = self.__ds.get_child(os.path.dirname(path))
            if ((not parent) or (not parent.is_collection())):
                self.__log(__name, '409 (parent not exists|collection)')
                return wdp.hr.http_409()
            else:
                resource = parent.mk_col(os.path.basename(path))
                if (resource):
                    self.__log(__name, '201 (ok)')
                    return wdp.hr.http_201(request.build_absolute_uri())
                else:
                    self.__log(__name, '403 (failed)')
                    return wdp.hr.http_403()
        self.__log(__name, 'unknown error')

    def	__copy_or_move(self, name, func, request, path):
        '''
        Process COPY WebDAV request.
        E.g.: cp /folder1/abc => /folder3/folder31/ at http://localhost:8000/
        "folder1/sdthdgjh" => "http://localhost:8000/folder3/folder31/sdthdgjh", Depth: 0
        Cases:
             Dst +  Over = 204
             Dst + !Over = 412
            !Dst + ?Over = 201/409
        TODO: ??? - failed to overwrite
        TODO: ds.resource.cp_to(replace)
        @return: http response:
          - 201	- ok (created)
          - 204	+ ok (replaced)
          - 403	+ src == dst
          - 404	+ src not exists
          - 409	+ dst parent collection not exists
          - 412	+ no overwrite but dst exists
          - 502	+ dst out of namespace
          - 403 - error (?..)
        '''
        __name = name
        dst_uri_quoted = request.META['HTTP_DESTINATION']
        dst_uri = unicode(urllib.unquote(dst_uri_quoted), 'utf-8').rstrip('/')   # just in case
        overwrite = (request.META.get('HTTP_OVERWRITE', 'T') != 'F')
        self.__log(__name, '"%s" => "%s", Over: %d', path, dst_uri, int(overwrite))
        src_uri = unicode(urllib.unquote(request.build_absolute_uri()), 'utf-8').rstrip('/')   # just in case
        src_head = src_uri[:-len(path)]     # e.g. http://localhost:8000/
        dst_path = dst_uri[len(src_head):]  # e.g. folder3/folder31/sdthdgjh
        #self.__log(__name, 'Scr: %s = %s + %s', src_uri, src_head, path)
        #self.__log(__name, 'Dst: %s = %s + %s', dst_uri, src_head, dst_path)
        # 1. check copy-to-self
        if (src_uri == dst_uri):
            self.__log(__name, '403 (src == dst)')
            return wdp.hr.http_403()
        # 2. check dst namespace
        if (not dst_uri.startswith(src_head)):
            self.__log(__name, '502 (dst out of namespace)')
            return wdp.hr.http_502()
        # 3. check src exists
        src = self.__ds.get_child(path)
        if (not src):
            self.__log(__name, '404 (src not exists)')
            return wdp.hr.http_404()
        # 4. check dst exists (204/412) or not (201/409)
        dst = self.__ds.get_child(dst_path)
        if (dst):   # dst exists => check over
            self.__log(__name, 'dst exists')
            if (not overwrite):
                self.__log(__name, '412 (dst exists)')
                return wdp.hr.http_412()
            # dst exists and can overwrite
            self.__log(__name, 'try to replace')
            if (func(src, dst_path)):
                self.__log(__name, '204 (ok, replaced)')
                return wdp.hr.http_204()
            self.__log(__name, '403 (failed)')
            return wdp.hr.http_403()    # FIXME: replacing failed - it's not 403
        else:       # dst not exists => check parent
            self.__log(__name, 'dst "%s" not exists', dst_path)
            parent = self.__ds.get_child(os.path.dirname(dst_path))
            if ((not parent) or (not parent.is_collection())):
                self.__log(__name, '409 (parent not exists|collection)')
                return wdp.hr.http_409()
            # parent exists and is collection
            self.__log(__name, 'try to create %s => %s', path, dst_path)
            if (func(src, dst_path)):
                self.__log(__name, '201 (ok, created)')
                return wdp.hr.http_201(dst_uri_quoted)
            self.__log(__name, '403 (failed)')
            return wdp.hr.http_403()    # FIXME: creating failed - it's not 403
        self.__log(__name, 'unknown error')

    def	__do_copy(self, request, path):
        '''
        Process COPY method.
        '''
        return self.__copy_or_move('COPY', self.__ds.copy, request, path)

    def	__do_move(self, request, path):
        '''
        Process MOVE method.
        '''
        return self.__copy_or_move('MOVE', self.__ds.move, request, path)
