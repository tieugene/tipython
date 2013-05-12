# -*- coding: utf-8 -*-1
'''
lansite.apps.file.webdav
DONE:
	MKCOL
	MOVE
	COPY
TODO:
FIXME:
	err handling
'''

from django.http import HttpResponse

def	options(request):
	response = HttpResponse(content_type = 'httpd/unix-directory')
	response['Allow'] = 'OPTIONS,GET,PUT,HEAD,POST,DELETE,TRACE,PROPFIND,PROPPATCH,COPY,MOVE,REPORTS'
	response['DAV'] = '1,2,addressbook-access'
	return response

def	propfind(request):
	'''
	Generates test WebDAV response
	1. parse request
	2. gen response:
		creationdate
		getlastmodified
		getcontenttype
		resourcetype
		getcontentlength (files only)
	2.1. add object info.
	2.2. if depth=1 and object=dir - add content
	'''
	depth = request.META.get('HTTP_DEPTH', None)
	# 1. parse request
	print "Path:", request.path_info
	print "Depth:", depth
	props = dict()
	body = request.read()
	print body
	dom = etree.fromstring(body)
	for i in list(list(dom)[0]):
		props[_gettagns(i.tag)[1]] = True
	# 2. generate response
	root = etree.Element('multistatus', xmlns='DAV:')
	realpath = __url2path(request.path_info)
	root.append(__fill_propfind(props.copy(), request.path_info))
	if (os.path.isdir(realpath) and depth == '1'):
		for i in (os.listdir(realpath)):
			root.append(__fill_propfind(props.copy(), request.path_info + i))
	return HttpResponse(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True), mimetype='text/xml; charset=utf-8')


davdict = {
	'OPTIONS':	options,	# HTTP+
#	'GET':		get,		# HTTP+
#	'HEAD':		head,		# HTTP?
#	'POST':		post,		# HTTP
#	'PUT':		put,		# HTTP+
#	'PATCH':			# HTTP-
#	'DELETE':	delete,		# HTTP+
#	'TRACE':	trace,		# HTTP-
#	'LINK':				# HTTP-
#	'UNLINK':			# HTTP-
	'PROPFIND':	propfind,	# WebDAV+
#	'PROPPATCH':	proppatch,	# WebDAV
#	'MKCOL':	mkcol,		# WebDAV
#	'COPY':		copy,		# WebDAV
#	'MOVE':		move,		# WebDAV
#	'LOCK':		lock,		# WebDAV-
#	'UNLOCK':	unlock,		# WebDAV-
}
