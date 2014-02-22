#!/bin/env python
# -*- coding: utf-8 -*-
'''
FIXME:
* clusters by domain
* and apps inside
'''

import urllib
from HTMLParser import HTMLParser

# 2. find
# найти тег
# выцепить подтег
# выцепить регексом нужное
# http://docs.python.org/2/library/htmlparser.html

def	chk(URL):
	class	MyHTMLParser(HTMLParser):
		def handle_starttag(self, tag, attrs):
			print "Encountered a start tag:", tag
		def handle_endtag(self, tag):
			print "Encountered an end tag :", tag
		def handle_data(self, data):
			print "Encountered some data  :", data.encode('utf-8')
	f = urllib.urlopen(URL)
	parser = MyHTMLParser()
	parser.feed(f.read().decode(f.headers.getparam('charset')))

def	chk_persw():
	'''
	PersW
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - found; 2 - EOL
		ver = None
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 0) and (tag == 'title'):
				self.state = 1
		def handle_data(self, data):
			if (self.state == 1):
				if data.startswith(')'):
					chunks = data.split(' ', 4)[1:4]
					self.ver = chunks[0].split('.',1)[1]
					self.date = chunks[2]
					self.state = 2

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.pfrf.ru/ot_peter/soft/5738.html')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_pdspu():
	'''
	(ПД СПУ 2010
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0: not found; 1: table; 2: strong, 3 - EOL
		ver = None
		date = None
		strongcount = 0
		def handle_starttag(self, tag, attrs):
			if (self.state == 0) and (tag == 'table'):
				self.state = 1
			elif (self.state == 1) and (tag == 'strong'):
				self.state = 2
				self.strongcount += 1
		def handle_endtag(self, tag):
			if (self.state == 1) and (tag == 'table'):
				self.state = 3
			if (self.state == 2) and (tag == 'strong'):
				self.state = 1
		def handle_data(self, data):
			if (self.state == 2):
				if (self.strongcount == 2):
					self.ver = data
				elif (self.strongcount == 4):
					self.date = data

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.pfrf.ru/ot_smolensk_soft/5256.html')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_nd():
	'''
	Возмещение НДС: Налогоплательщик
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - found; 2 - EOL
		ver = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 0) and (tag == 'title'):
				self.state = 1
		def handle_data(self, data):
			if (self.state == 1):
				self.ver = data.rsplit(' ', 1)[1]
				self.state = 2

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.gnivc.ru/software/free_software/software_ul_fl/compensation_vat/')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver

def	chk_kladr():
	'''
	КЛАДР
	<div class="content"> > <div> > after br #2
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0: not found; 1: found div; 2: found div#2, 3: found br, 4: EOL
		ver = None
		date = None
		brcount = 0
		def handle_starttag(self, tag, attrs):
			if (self.state == 4):
				return
			elif (self.state == 0):
				if (tag == 'div') and (attrs == [('class', 'content')]):
					self.state = 1
			elif (self.state == 1):
				if (tag == 'div'):
					self.state = 2
			elif (self.state == 2):
				if (tag == 'br'):
					self.brcount += 1
		def handle_data(self, data):
			if (self.state == 2):
				if (self.brcount == 1):
					self.ver = data.split(' ')[1].strip()
				elif (self.brcount == 2):
					self.date = data.split('-')[1].strip()
					self.state = 4

	parser = MyHTMLParser()
	f = urllib.urlopen('http://gnivc.ru/inf_provision/classifiers_reference/kladr/')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_tconp():
	'''
	ТС-Обмен
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - found; 2 - EOL
		ver = None
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 0) and (tag == 'title'):
				self.state = 1
		def handle_data(self, data):
			if (self.state == 1):
				chunks = data.rsplit(' ', 3)[1:]
				self.ver = chunks[0]
				self.date = chunks[2]
				self.state = 2

	# 1. get page
	#params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
	#f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query", params)
	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.gnivc.ru/software/free_software/software_ul_fl/cu_np_exchange/')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date
	# 3. compare with db
	# 4. store compared
	# 5. show result

def	chk_decl2013():
	'''
	Декларация 2013
	# 0: not found; 1: found <div class="section-row">, 2: found <div>, 9 - EOL
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0
		ver = None
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 9): return
			elif (self.state == 0) and (tag == 'div'):
				if (attrs == [('class', 'section-row')]):
					self.state = 1
			elif (self.state == 1) and (tag == 'div'):
				self.state = 2
		def handle_data(self, data):
			if (self.state == 9): return
			if (self.state == 2):
				chunks = data.strip().rsplit(' ', 3)[1:]
				self.ver = chunks[0]
				self.date = chunks[2]
				self.state = 9
				return

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.gnivc.ru/software/free_software/software_fl/ndfl_3_4/')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_nds():
	'''
	Налогоплательщик
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - found; 2 - EOL
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 0) and (tag == 'div') and (attrs == [('id', 'vers')]):
				self.state = 1
		def handle_data(self, data):
			if (self.state == 1):
				self.date = data.rstrip()
				self.state = 2
				#self.reset()

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.nalogy.ru/download.html')
	parser.feed(f.read().decode('utf-8'))
	print parser.date

def	chk_pnv():
	'''
	ПНВ
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - <a> found; 2: </a> found>, 9: EOL
		ver = None
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 9):
				return
			if (self.state == 0) and (tag == 'a') and (attrs == [('id', 'LastVersion'), ('name', 'LastVersion')]):
				self.state = 1
		def handle_endtag(self, tag):
			if (self.state == 9):
				return
			elif (self.state == 1) and (tag == 'a'):
				self.state = 2
		def handle_data(self, data):
			if (self.state == 9):
				return
			elif (self.state == 2):
				chunks = data.split(' ')[1:]
				self.ver = chunks[0]
				self.date = chunks[2]
				self.state = 9

	parser = MyHTMLParser()
	f = urllib.urlopen('http://rpn.gov.ru/node/5523')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_sbis():
	'''
	СБиС
	<p>Текущая версия программы: <b>2.4.195 от 18.02.2014</b>
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0	# 0 - not found; 1 - <p> found; 2: "Текущая версия программы:", 3: <b> found, 9: EOL
		ver = None
		ver = None
		date = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 9): return
			elif (self.state == 0):
				#print tag
				if (tag == 'p'):
					self.state = 1
			elif (self.state == 2):
				if (tag == 'b'):
					self.state = 3
		def handle_endtag(self, tag):
			if (self.state == 9): return
			elif (self.state == 1) and (tag == 'p'):
				self.state = 0
		def handle_data(self, data):
			if (self.state == 9): return
			elif (self.state == 1):
				data = data.strip()
				if (data == u'Текущая версия программы:'):
					self.state = 2
			elif (self.state == 3):
				self.state = 9
				chunks = data.split(' ',)
				self.ver = chunks[0].strip()
				self.date = chunks[2].strip()

	parser = MyHTMLParser()
	f = urllib.urlopen('http://sbis.ru/download/update')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver, parser.date

def	chk_xml(tofind):
	'''
	ChkXML
	in div class="item2" > <h1>CheckXML+2НДФЛ 2013</h1> - <div class="ver">Дата версии:<br><b>18.02.2014</b></div>
	states:
	- 0: not found
	- 1: <div class="item2"> found
	- 2: <h1> found
	- 3: "CheckXML+2НДФЛ 2013" found
	- 4: <div class="ver"> found
	- 5: <b> found
	- 9: EOL
	'''
	TOFIND = tofind
	class	MyHTMLParser(HTMLParser):
		state = 0
		date = None
		divcount = 0
		def handle_starttag(self, tag, attrs):
			if (self.state == 9): return
			elif (self.state == 0):
				if (tag == 'div') and (attrs == [('class', 'item2')]):
					#print "1. item2"
					self.state = 1
					self.divcount = 1
			else:	# self.state == 1..8
				if (tag == 'div'):
					self.divcount += 1
					#print "DIV:", self.divcount, attrs
				if (self.state == 1):
					if (tag == 'h1'):
						#print "2. <h1>"
						self.state = 2
				elif (self.state == 3):
					if (tag == 'div'):
						if (attrs == [('class', 'ver')]):
							#print "4. ver"
							self.state = 4
				elif (self.state == 4):
					if (tag == 'b'):
						#print "b"
						self.state = 5
		def handle_endtag(self, tag):
			if (self.state == 9): return
			elif (self.state > 0) and (tag == 'div'):
				self.divcount -= 1
				#print "/DIV:", self.divcount
				if (self.divcount == 0):
					self.state = 0
		def handle_data(self, data):
			if (self.state == 9): return
			elif (self.state == 2):
				data = data.strip()
				#print data
				if (data == TOFIND):
					#print "3. CheckXML"
					self.state = 3
			elif (self.state == 5):
				#print "Version:", data
				self.state = 9
				self.date = data

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.buhsoft.ru/?title=download.php')
	content = f.read().decode('windows-1251')
	parser.feed(content)
	print parser.date

def	chk_chkxml():
	chk_xml(u'CheckXML')

def	chk_chkxmlufa():
	chk_xml(u'CheckXML-UFA')

def	chk_chkxmlndfl():
	chk_xml(u'CheckXML+2НДФЛ 2013')

def	chk_java():
	'''
	Java
	in <div class="jvc0w2"> > <strong>
	States:
	0: not found
	1: found <div class="jvc0w2">
	2: found <strong>
	9: EOL
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0
		ver = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 9): return
			elif (self.state == 0) and (tag == 'div') and (attrs == [('class', 'jvc0w2')]):
				self.state = 1
			elif (self.state == 1) and (tag == 'strong'):
				self.state = 2
		def handle_data(self, data):
			if (self.state == 9): return
			if (self.state == 2):
				self.state = 9
				chunks = data.strip().split(' ')[2:]
				self.ver = chunks[0]+'.'+chunks[2]

	parser = MyHTMLParser()
	f = urllib.urlopen('http://www.java.com/ru/download/manual.jsp')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver

def	chk_alko():
	'''
	Декларант-Алко
	in <div id="wiki-post-content"> after <h2><span>Росалкогольрегулирование</span></h2> > <li> > <a> Декларант-Алко
	States:
	0: not found
	1: found <div id="wiki-post-content">
	2: found <h2>
	3: found <span>
	4: found Росалкогольрегулирование
	5: found li
	6: found a
	9: EOL
	'''
	class	MyHTMLParser(HTMLParser):
		state = 0
		ver = None
		def handle_starttag(self, tag, attrs):
			if (self.state == 9): return
			elif (self.state == 0) and (tag == 'div') and (attrs == [('id', 'wiki-post-content')]):
					self.state = 1
			elif (self.state == 1) and (tag == 'h2'):
				self.state = 2
			elif (self.state == 2) and (tag == 'span'):
				self.state = 3
			elif (self.state == 4) and (tag == 'li'):
				self.state = 5
			elif (self.state == 5) and (tag == 'a'):
				self.state = 6
		def handle_endtag(self, tag):
			if (self.state == 9): return
			elif (self.state == 2) and (tag == 'h2'):
				self.state = 1
			elif (self.state == 3) and (tag == 'span'):
				self.state = 2
			elif (self.state == 5) and (tag == 'li'):
				self.state = 4
			elif (self.state == 6) and (tag == 'a'):
				self.state = 5
		def handle_data(self, data):
			if (self.state == 9): return
			if (self.state == 3):
				data = data.strip()
				if (data == u'Росалкогольрегулирование'):
					self.state = 4
			if (self.state == 6):
				data = data.strip()
				if data.startswith(u'Декларант-Алко'):
					self.state = 9
					self.ver = data.split(' ')[1]

	parser = MyHTMLParser()
	f = urllib.urlopen('https://dap.center-inform.ru/tehpod/faq/%D0%A6%D0%B5%D0%BD%D1%82%D1%80+%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8/')
	parser.feed(f.read().decode(f.headers.getparam('charset')))
	print parser.ver

#chk('https://dap.center-inform.ru/tehpod/faq/%D0%A6%D0%B5%D0%BD%D1%82%D1%80+%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8/')
#chk_persw()
#chk_pdspu()
#chk_nd()
#chk_kladr()
#chk_tconp()
#chk_nds()
#chk_pnv()
#chk_decl2013()
#chk_sbis()
#chk_chkxml()
#chk_chkxmlufa()
#chk_chkxmlndfl()
#chk_java()
#chk_alko()
