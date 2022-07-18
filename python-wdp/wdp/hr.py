# -*- coding: utf-8 -*-
'''
HTTP responses. See wiki to expand.
HttpResponse(content='', content_type=None, status=200)
@undocumented: __package__
'''

#import urllib
import wdp.const

#from wdp.util import LOG, pprintxml

def	__http(status, content=None, content_type=None, head=None):
    '''
    Common http response.
    '''
    from django.http import HttpResponse
    if (content != None):
        response = HttpResponse(content=content, content_type=content_type, status=status)
        response['Content-Length'] = len(content)
    else:
        response = HttpResponse(status=status)
    if (head):
        for key, value in head.iteritems():
            response[key] = value
    return response

def	http_200(content='', content_type=None, head=None):
    '''
    HTTP:	OK
    @param content:any - response body
    @param content_type:str - mime
    @param head:dict - response header addons
    '''
    return __http(status=200, content=content, content_type=content_type, head=head)

def	http_201(location):
    '''
    HTTP:	Created
    TODO: ETag
    @param location:uri - full uri of created resource
    '''
    return __http(status=201, head={'Location': location})

def	http_204():
    '''
    HTTP:	No Content
    '''
    return __http(status=204)

def	http_206(content, content_type, head):
    '''
    HTTP:	Partial Content
    '''
    return __http(status=206, content=content, content_type=content_type, head=head)

def	http_207(body):
    '''
    WebDAV:	Multi-Status
    @param body:str - response xml
    '''
    #LOG(pprintxml_s(body))
    return __http(status=207, content=body, content_type=wdp.const.MIME_XML)

def	http_304(etag=None):
    '''
    HTTP:	Not Modified
    @param etag:str - ETag
    '''
    return __http(status=304, head={'Etag': etag} if etag else None)

def	http_400():
    '''
    HTTP:	Bad Request
    '''
    return __http(status=400)

def	http_401():
    '''
    HTTP:	Acces Denied
    '''
    return __http(status=401)

def	http_403(body=None):
    '''
    HTTP:	Forbidden
    @param body:str - xml of precondition error
    '''
    return __http(status=403, content=body, content_type=wdp.const.MIME_XML if body else None)

def	http_404(path=None):
    '''
    HTTP:	Not Found
    '''
    return __http(status=404, content='"%s" not exists' if path else None)

def	http_405(allowed):
    '''
    HTTP:	Method Not Allowed.
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html 10.4.6
    @param allowed:str - method allowed
    '''
    return __http(status=405, head={'Allowed': allowed})

def	http_409(body=None):
    '''
    HTTP:	Conflict
    @param body:str - xml of precondition error
    '''
    return __http(status=409, content=body, content_type=wdp.const.MIME_XML if body else None)

def	http_412(body=None):
    '''
    HTTP:	Precondition Failed
    @param body:str - xml of precondition error
    '''
    return __http(status=412, content=body, content_type=wdp.const.MIME_XML if body else None)

def	http_415():
    '''
    HTTP:	Unsupported Media Type
    '''
    return __http(status=415)

def	http_416():
    '''
    HTTP:	Requested Range Not Satisfiable
    @param size:int - real resource size
    '''
    return __http(status=416)

def	http_422():
    '''
    WebDAV: Unprocessable Entity
    '''
    return __http(status=422)

def	http_423(body):
    '''
    WebDAV:	Locked
    @param body:str - xml of precondition error
    '''
    return __http(status=423, content=body, content_type=wdp.const.MIME_XML)

def	http_502():
    '''
    HTTP:	Bad gateway
    '''
    return __http(status=502)

def	http_507():
    '''
    WebDAV:	Insufficient Storage
    '''
    return __http(status=507)
