# -*- coding: utf-8 -*-
# const.py
'''
Error codes.
@undocumented: __package__
'''

# DavStrage return codes

DS_OK = 0     # OK
DS_NA = 1     # Not Allowed - operation not allowed at all - raise http 405)
DS_PD = 2     # Access Denied [for this user] - raise ???
DS_NF = 5     # Not Found - raise http 404
#DS_NI = ?     # Not Implemented (405?)

# Mime types
MIME_XML = 'text/xml; charset="utf-8"'  # XML mime
MIME_FOLDER = 'httpd/unix-directory'    # Folder mime
MIME_EMPTY = 'inode/x-empty'            # Empty file mime

# OPTIONS (http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)
# (X) means "not implemented yet"
# merge: OPT_ALL=OPT_GET|OPT_PUT|...
# can OPT_X: OPT_ALL&OPT_X
OPT_GET = 1             # HTTP
OPT_HEAD = 2            # HTTP  (X)
OPT_POST = 4            # HTTP  (X)
OPT_PUT = 8             # HTTP
OPT_DELETE = 16         # HTTP
OPT_TRACE = 32          # HTTP  (X)
OPT_CONNECT = 64        # HTTP  (X)
OPT_PROPFIND = 128      # WebDAV
OPT_PROPPATCH = 256     # WebDAV  (X)
OPT_MKCOL = 512         # WebDAV
OPT_COPY = 1024         # WebDAV
OPT_MOVE = 2048         # WebDAV
OPT_LOCK = 4096         # WebDAV; +UNLOCK
