#!/bin/env python
# -*- coding: utf-8 -*-
'''
http://docs.wand-py.org
'''

import urllib
from HTMLParser import HTMLParser

URL = "http://www.gnivc.ru/software/free_software/software_ul_fl/cu_np_exchange/"

# 1. get page
#opener = urllib.FancyURLopener({})
#f = opener.open(URL)
#content = f.read()


'''
connection = urllib.urlopen(query + search)
            encoding = connection.headers.getparam('charset')
            page = connection.read().decode(encoding)
'''
#params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query", params)
f = urllib.urlopen(URL)
encoding = f.headers.getparam('charset')
content = f.read().decode(encoding)

# 2. find
# найти тег
# выцепить подтег
# выцепить регексом нужное
# http://docs.python.org/2/library/htmlparser.html


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :", data.encode('utf-8')

parser = MyHTMLParser()
parser.feed(content)

# 3. compare with db
# 4. store compared
# 5. show result
