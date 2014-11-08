#!/bin/env python
# -*- coding: utf-8 -*-
'''
'''

# 1. 3rd parties
import web
# 2. system
import sys, os, datetime
# hack
sys.path.append(os.path.dirname(__file__))
# 3. my
from sqltpl import *

reload(sys)
sys.setdefaultencoding('utf-8')

# defaults
debug	= True
cache	= False
db	= 'data.db'
token	= 'putsomethinghere'
try:
        from local_settings import *
except ImportError:
        pass
db = web.database(dbn='sqlite', db=db)
render = web.template.render('tpl/', cache=cache)

urls = (
	'/', 						'index',
	'/d/(\d{8})/',					'day',	# /<YYYY-MM-DD>/
	'/d/(\d{8})/i/(\d+)/',				'host',	# /<YYYY-MM-DD>/i/<ip>/
	'/d/(\d{8})/i/(\d+)/p/(\d+)/(\d+)/(\d{1})/',	'port',	# /<YYYY-MM-DD>/i/<ip>/p/<proto>/<port>/<dir>/
)

class	index:
	'''
	Show days (desc) with in/out
	'''
	def	GET(self):
		return render.index(db.query(tpl_index))

class	day:
	'''
	Show hosts (asc) with in/out for a day
	'''
	def	GET(self, date):
		return render.day(date, db.query(tpl_day_ip % date), db.query(tpl_day_hour % date), db.query(tpl_day_oport % date))

class	host:
	'''
	Show proto/dstport/dstip (asc) with in/out for a day/host
	'''
	def	GET(self, date, host):
		ip = long(host)
		return render.host(date, ip, db.query(tpl_host_srcport % (date, ip)), db.query(tpl_host_dstport % (date, ip)))

class	port:
	'''
	Show dstip (asc) with in/out for a day/host/proto/(s|d)port
	'''
	def	GET(self, date, host, proto, port, dir):
		ip = long(host)
		proto = int(proto)
		port = int(port)
		dir = int(dir)	# 0-i, 1-d)
		data = db.query(tpl_host_port_dstip % (date, ip, proto, 'oport' if dir else 'iport', port))
		return render.port(date, ip, proto, port, data)

# standalone
if __name__ == '__main__':
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(urls, globals()).wsgifunc()
