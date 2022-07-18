WDP - webdavprovider
This is not http-server itself - this is interface between http-server and DavStorage.
RFC 4918

= TODO constantly:
    * regen doc:    epydoc --html --graph=all wdp

= Install =
Deps: python-lxml, python-magic

= DavProvider =
Register for _sub_ uri w/ given DavStorage class.
Has dispatcher and functions for handling DAV requests.
Each handler: request?, [sub-]uri, user (pass transparently to DS)

= DavStorage =
Provides DP backend - maps request to data and data props to response.
Is like "callback" for DavProvider.
Classes:
	* Resource - parent
	* Collection(Resource):
	* Member(Resource)

= Notes =
* MUST=Required, SHOULD=Recomended, MAY=Optional
* Used DAV ns only.
* Depth = infinity (recomended); but no depth = infinity (optional)
* Collection/ - optional; 301 - optional

= ToDo =
* Examples:
	* Frontend=django
	* Frontend=BaseHTTPServer
	* Backend=FS
	* Backend=?
* Benchmarks
* docs
* setup (for lib)
* register namespaces and property map

= Ideas =
* Common xml parser: xml=>dict/list
* path=>tuple
* Collection - lazy cache?
* Collection - dict-like?

= To find =
* lock: exclusive by same user
* lock: shared - misc uuids?

Test:
	tcpdump -i lo -n -nn -vvv -w - 'host 127.0.0.1 and port 80'

= Index =
* testdav - example using mod_dav + web-pages

= PROPFIND =

Request:
    1. None
    2. <propfind>:
        <prop>:
            <_propname_/>
    3. <propfind>:
        <prpname/>
    4. <propfind>:
        <allprop/>
        [<include>:
            <_propname_/>
        ]
Response:
    multistatus:
        response+:
            href
            propstat:
                status
                prop:
                    _property_
Properties:
    creationdate		# datetime					(1)
    [displayname]
    [getcontentlanguage]
    getcontentlength	# 0|get_size()					(2)
    getcontenttype		# inplace: 'httpd/unix-directory'|get_mime()	(3)
    getlastmodified		# datetime					(2)
    lockdiscovery		# inplace: <lockdiscovery/>
    resourcetype		# inplace: <resourcetype><collection/>|<resourcetype/>
    supportedlock		# inplace: 2 x <lockentry>: <lockscope>:..., <locktype>:...
Algo:
    get resource. if it is:
    get resource.props
    fill reply
    if depth=1:
        for child in resource.children:
            get child.props
            fill reply
    fill 404
