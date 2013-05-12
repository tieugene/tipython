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
from django.core.urlresolvers import reverse, resolve

from lxml import etree
from xdg import Mime
import sys, os, shutil, datetime, pprint

__dav_url = '/file/dav/'
__dav_dir = '/mnt/shares/ftp/'

def	options(request):
	response = HttpResponse(content_type = 'httpd/unix-directory')
	response['Allow'] = 'OPTIONS,GET,PUT,HEAD,POST,DELETE,TRACE,PROPFIND,PROPPATCH,COPY,MOVE'
	response['DAV'] = '1,2,<http://apache.org/dav/propset/fs/1>'
	return response

def	__url2path(url):
	'''
	Converts requested URL into real path
	'''
	return __dav_dir + (url[(len(__dav_url)):])

def	__fill_propfind(props, url):
	'''
	Fills response by real file/dir attributes
	@param props:dict - requested properties
	@param url:strl - relative url
	@return lxml.etree.Element
	'''
	realpath = __url2path(url)
	response = etree.Element('response')
	etree.SubElement(response, 'href').text = url
	# 1. usable values
	propstat = etree.SubElement(response, 'propstat')
	prop = etree.SubElement(propstat, 'prop')
	if ('creationdate' in props):
		etree.SubElement(prop, 'creationdate').text = datetime.datetime.fromtimestamp(os.path.getctime(realpath)).strftime('%Y-%m-%dT%H:%M:%SZ')
		del props['creationdate']
	if ('getlastmodified' in props):
		# 'Mon, 11 Apr 2011 04:03:09 GMT'
		# FIXME: GMT
		etree.SubElement(prop, 'getlastmodified').text = datetime.datetime.fromtimestamp(os.path.getmtime(realpath)).strftime('%a, %d %b %Y %H:%M:%S GMT')
		del props['getlastmodified']
	if (os.path.isdir(realpath)):
		if ('getcontenttype' in props):
			etree.SubElement(prop, 'getcontenttype').text = 'httpd/unix-directory'
			del props['getcontenttype']
		if ('resourcetype' in props):
			etree.SubElement(etree.SubElement(prop, 'resourcetype'), 'collection')
			del props['resourcetype']
	else:
		if ('getcontentlength' in props):
			etree.SubElement(prop, 'getcontentlength').text = str(os.path.getsize(realpath))
			del props['getcontentlength']
		if ('getcontenttype' in props):
			etree.SubElement(prop, 'getcontenttype').text = str(Mime.get_type(realpath))
			del props['getcontenttype']
		if ('resourcetype' in props):
			etree.SubElement(prop, 'resourcetype')
			del props['resourcetype']
	etree.SubElement(propstat, 'status').text = 'HTTP/1.1 200 OK'
	# 2. unusable values
	propstat = etree.SubElement(response, 'propstat')
	prop = etree.SubElement(propstat, 'prop')
	for i in props:
		etree.SubElement(prop, i)
	etree.SubElement(propstat, 'status').text = 'HTTP/1.1 404 Not Found'
	return response

def	_gettagns(tag):
	""" returns a tuple of namespace,name """
	if tag[:1] == "{":
		return tag[1:].split("}", 1)
	else:
		return (None,tag)

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
	body = request.read()
	print "PROPFIND:"
	print "Path:", request.path_info
	print "Depth:", depth
	print "Body:", body
	props = dict()
	#print body
	'''
	dom = xml.dom.minidom.parseString(body)
	print dom.toxml()
	for i in dom.firstChild.firstChild.childNodes:
		print i.namespaceURI, i.localName
		props[i.localName] = True
	#a = dom.xpath('/D:propfind/D:prop/*', namespaces = {'D': 'DAV:'})
	'''
	dom = etree.fromstring(body)
	for i in list(list(dom)[0]):
		props[_gettagns(i.tag)[1]] = True
	# 2. generate response
	root = etree.Element('multistatus', xmlns='DAV:')
	#print props
	realpath = __url2path(request.path_info)
	root.append(__fill_propfind(props.copy(), request.path_info))
	if (os.path.isdir(realpath) and depth == '1'):
		for i in (os.listdir(realpath)):
			root.append(__fill_propfind(props.copy(), request.path_info + i))
	return HttpResponse(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True), mimetype='text/xml; charset=utf-8')

def	get(request):
	realpath = __url2path(request.path_info)
	file = open(realpath)
	response = HttpResponse(content = file.read(), content_type = str(Mime.get_type(realpath)))
	response['Last-Modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(realpath)).strftime('%a, %d %b %Y %H:%M:%S GMT')
	response['Accept-Ranges'] = 'bytes'
	response['Content-Length'] = str(os.path.getsize(realpath))
	return response

def	put(request):
	'''
	Location
	Statuscode: 201
	Content-Length
	Content-Type
	'''
	realpath = __url2path(request.path_info)
	file = open(realpath, "w")
	file.write(request.read())
	file.close()
	response = HttpResponse(status = 201, content_type = str(Mime.get_type(realpath)))
	response['Location'] = request.path_info
	response['Content-Length'] = str(os.path.getsize(realpath))
	return response

def	delete(request):
	'''
	'''
	realpath = __url2path(request.path_info)
	response = HttpResponse(status = 204, content_type = str(Mime.get_type(realpath)))
	response['Location'] = request.path_info
	response['Content-Length'] = '0'
	if (os.path.isdir(realpath)):
		shutil.rmtree(realpath)
	else:
		os.remove(realpath)
	return response

def	mkcol(request):
	realpath = __url2path(request.path_info)
	os.mkdir(realpath)
	response = HttpResponse(status = 201)
	return response

def	move(request):
	'''
	Destination
	HTTP_DEPTH: infinity
	HTTP_OVERWRITE: F
	NOTE: set django.root for test
	#pprint.pprint(request.META)
	print "Depth:", request.META['HTTP_DEPTH']		# infinity
	print "Overwrite:", request.META['HTTP_OVERWRITE']	# F
	#print "Path:", request.path
	print "Path info:", request.path_info			# == request.get_full_path()
	print "Full URI:", request.build_absolute_uri()
	print "Dest:", request.META['HTTP_DESTINATION']
	print "Body:", request.read()
	print "Src:", realpath_src
	print "Dst:", request.build_absolute_uri()[:-len(request.path_info)]
	'''
	realpath_src = __url2path(request.path_info)
	realpath_dst = __url2path(request.META['HTTP_DESTINATION'][len(request.build_absolute_uri()[:-len(request.path_info)]):])
	os.rename(realpath_src, realpath_dst)
	response = HttpResponse(status = 201)
	return response

def	copy(request):
	realpath_src = __url2path(request.path_info)
	realpath_dst = __url2path(request.META['HTTP_DESTINATION'][len(request.build_absolute_uri()[:-len(request.path_info)]):])
	if (os.path.isdir(realpath_src)):
		shutil.copytree(realpath_src, realpath_dst)
	else:
		shutil.copy2(realpath_src, realpath_dst)
	response = HttpResponse(status = 201)
	return response

davdict = {
	'OPTIONS':	options,	# HTTP+
	'GET':		get,		# HTTP+
#	'HEAD':		head,		# HTTP?
#	'POST':		post,		# HTTP
	'PUT':		put,		# HTTP+
#	'PATCH':			# HTTP-
	'DELETE':	delete,		# HTTP+
#	'TRACE':	trace,		# HTTP-
#	'LINK':				# HTTP-
#	'UNLINK':			# HTTP-
	'PROPFIND':	propfind,	# WebDAV+
#	'PROPPATCH':	proppatch,	# WebDAV
	'MKCOL':	mkcol,		# WebDAV
	'COPY':		copy,		# WebDAV
	'MOVE':		move,		# WebDAV
#	'LOCK':		lock,		# WebDAV-
#	'UNLOCK':	unlock,		# WebDAV-
}
