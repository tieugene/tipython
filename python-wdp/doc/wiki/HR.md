TODO: merge all into common table Status x Method = body/ctype/head

# 200 _HTTP OK_ #

| **Method** | **Body** | **Ctype** | **Head** |
|:-----------|:---------|:----------|:---------|
| OPTIONS    | _None_   | unix/dir  | Allow <br /> DAV <br />[MS\_Author-Via] |
| GET        | _file_   | _mime_    | Last-Modified <br /> Accept-Ranges: 'bytes' |
| LOCK       | _xml_    | text/xml  | [Lock-Token] |
|            |          |           |          |

# 201 _HTTP Created_ #

| **Method** | **Body** | **Ctype** | **Head** |
|:-----------|:---------|:----------|:---------|
| MKCOL      | -        | ?         | Location |
| PUT        | -        | ?         | Location |
| COPY       | -        | -         | ?        |
| MOVE       | -        | -         | Location |
| LOCK       | _xml_    | xml       | ?        |

_Note: LOCK - unmapped resource_

# 204 _HTTP No Content_ #

Methods: PUT, COPY, MOVE, UNLOCK

~~Body, CType, Head~~

_Note: COPY - replacing_

# 207 _WebDAV Multi-Status_ #

Methods: PROPFIND, PROPPATCH, COPY, MOVE, LOCK

CType: application/xml; charset="utf-8"

Body: xml

~~Head~~

# 304 _HTTP Not Modified_ #

Methods: GET

Head: ETag

~~Body, Head~~

# 400 _HTTP Bad Request_ #

Methods: All

~~Body, CType, Head~~

# 403 _HTTP Forbidden_ #

Method: PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, UNLOCK

[Body: xml (precondition error)

[CType: xml]

~~Head~~

# 404 _HTTP Not Found_ #

Methods: PROPFIND, PROPPATCH, DELETE, GET, COPY, MOVE, UNLOCK?

~~Body, Ctype, Head~~

_Note: but can include html page_

# 405 _HTTP Method Not Allowed_ #

Methods: MKCOL, PUT

Head: Allowed

~~Body, Ctype~~

# 409 _HTTP Conflict_ #

Method: MKCOL, PUT, COPY, MOVE, LOCK, UNLOCK

[Body: xml (precondition error)

[CType: xml]

~~Head~~

# 412 _HTTP Precondition Failed_ #

Method: COPY, MOVE, LOCK

[Body: xml (precondition error)

[CType: xml]

~~Head~~

# 415 _HTTP Unsupported Media Type_ #

Method: MKCOL

~~Body, Ctype, Head~~

# 422 _WebDAV Unprocessable Entity_ #

~~Body, Ctype, Head~~

# 423 _WebDAV Locked_ #

Method: COPY, MOVE, LOCK

Body: xml (precondition error)

CType: xml

~~Head~~

# 502 _HTTP Bad gateway_ #

Method: COPY, MOVE (to resource out of current site)

~~Body, Ctype, Head~~

# 507 _WebDAV Insufficient Storage_ #

Method: MKCOL, COPY

~~Body, Ctype, Head~~