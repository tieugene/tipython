#!/bin/env python
# -*- coding: utf-8 -*-
'''
testdav.py - tool to test WebDAV servers: make right and wrong requests - and saves responces.
Apache:
./testdav.py http://localhost/trash/ apache [/mnt/shares/dasarchive/inbox]
./testdav.py http://localhost/testwdp/ test [/mnt/shares/testwdp]
python testdav.py http://localhost:8000/ test [/mnt/shares/testwdp]
'''
# 1. system
import os, sys, pprint

# 2. 3rd parties
import requests, tidy

reload(sys)
sys.setdefaultencoding('utf-8')

def prepare(path):
    '''
    Prepare outdir and realpath to work:
    * Remove all
    * Create rw, ro and hidden dirs.
    * Create rw, ro and hidden files.
    '''
    pass

def __save_response(no, outdir, rtype, url, headers=None):
    '''
    Make request and save response to file
    @param no: test number
    @param outdir
    '''
    r = requests.request(rtype, url, headers=headers)
    outfile = open(os.path.join(outdir, '%s.%02d' % (rtype, no)), 'wb')
    tosave = ''
    tosave += 'HTTP/1.1 %s %s\n' % (r.status_code, r.raw.reason)
    for k, v in r.headers.iteritems():
        tosave += '%s: %s\n' % (k, v)
    outfile.write(tosave)
    if (r.content):
        if (r.status_code == 207):
            #xml = etree.fromstring(r.content)
            content = str(tidy.parseString(r.content, **{'output_xml':1, 'indent':1, 'input_xml':1}))
        else:
            content = r.content
        outfile.write(content)
    outfile.close()

def chk_options(url, outdir):
    '''
    Test:
    * root
    * ordinar dir
    * ordinar file
    * access denied dir
    * its child
    * inexistant resource
    Results:
    * 403 - access denied
    * 200 - other
    '''
    paths = (
        '',
        'folder',
        'test.txt',
        'folder0',          # rwx------
        'folder0/folder00', # acces denied
        'qwerty',           # not exists
    )
    for i, path in enumerate(paths):
        __save_response(i, outdir, 'OPTIONS', url+path)

def chk_get(url, outdir, start=None, end=None):
    '''
    Test:
    * ordinar dir
    * ordinar file
    * empty file
    * access denied file
    * access denied dir
    * its child
    * inexistant resource
    Results:
    * 200 - ok
    * 403 - access denied
    * 404 - not found
    '''
    paths = (
        '',
        'folder',
        'test.txt',
        'file.txt',         # empty
        'protected.txt',    # access denied
        'folder0',          # rwx------
        'folder0/folder00', # acces denied
        'qwerty',           # not exists
    )
    for i, path in enumerate(paths):
        __save_response(i, outdir, 'GET', url+path)

def chk_get_partial(url, outdir):
    '''
    Results:
    * 200 - ok
    * 403 - access denied
    * 404 - not found
    * 206 - partial get
    * 416 - out of range
    '''
    path = 'test.txt'
    ranges = (
        # ok
        ('0', '4'),         # 1st 5 bytes
        ('5', '9'),         # 2nd 5 bytes
        ('5', ''),          # from 5 to end
        ('', '5'),          # last 5 bytes
        ('5', '20'),        # last 5 bytes (truncated)
        # bad
        ('20', ''),         # 416
        ('5', '1'),         # 200
        ('qwer', 'qwer'),   # bad request
    )
    for i, j in enumerate(ranges):
        __save_response(i, outdir, 'GET', url+path, headers={'Range': 'bytes=%s-%s' % j})

def chk_head(url, outdir):
    '''
    Test:
    * ordinar dir
    * ordinar file
    * empty file
    * readonly file
    * readonly dir
    * access denied file
    * access denied dir
    * its child
    * inexistant resource
    Results:
    * 200 - ok
    * 403 - access denied
    * 404 - not found
    '''
    paths = (
        '',
        'folder',
        'test.txt',
        'file.txt',         # empty
        'protected.txt',    # access denied
        'folder0',          # rwx------
        'folder0/folder00', # acces denied
        'qwerty',           # not exists
    )
    for i, path in enumerate(paths):
        __save_response(i, outdir, 'HEAD', url+path)

def chk_post(url, outdir):
    pass

def chk_put(url, outdir):
    '''
    Test:
    * ordinar dir
    * ordinar file
    * empty file
    * access denied file
    * access denied dir
    * its child
    * inexistant resource
    Results:
    * 200 - ok
    * 403 - access denied
    * 404 - not found
    '''
    pass

def chk_delete(url, outdir):
    pass

def chk_trace(url, outdir):
    pass

def chk_propfind(url, outdir):
    paths = (
        #'',
        'folder1',
        #'test.txt',
        #'file.txt',         # empty
        #'protected.txt',    # access denied
        #'folder0',          # rwx------
        #'folder0/folder00', # acces denied
        #'qwerty',           # not exists
    )
    for i, path in enumerate(paths):
        __save_response(i, outdir, 'PROPFIND', url+path, headers={'Depth': '1'})

def chk_proppatch(url, outdir):
    pass

def chk_mkcol(url, outdir):
    pass

def chk_copy(url, outdir):
    '''
    * root
    * rw/ro/hidden/unexistant dir x Depth = undef/0/1
    * rw/ro/hidden/unexistant file x Depth = undef/0/1
    '''
    pass

def chk_move(url, outdir):
    pass

def main(url, outdir, realpath=None):
    if (realpath):
        prepare(realpath)
    # HTTP
    chk_options(url, outdir)
    #chk_get(url, outdir)
    #chk_get_partial(url, outdir)
    #chk_head(url, outdir)
    #chk_post(url, outdir)
    #chk_put(url, outdir)
    #chk_delete(url, outdir)
    #chk_trace(url, outdir)
    # WebDAV
    #chk_propfind(url, outdir)
    #chk_proppatch(url, outdir)
    #chk_mkcol(url, outdir)
    #chk_copy(url, outdir)
    #chk_move(url, outdir)

if (__name__ == '__main__'):
    argc = len(sys.argv)
    if ((argc < 3) or (argc > 4)):
        print 'Usage: %s <url> <outdir> [<realpath>]' % sys.argv[0]
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3] if (argc > 3) else None)
