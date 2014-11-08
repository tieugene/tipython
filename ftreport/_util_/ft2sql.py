#!/bin/env python
# -*- coding: utf-8 -*-
'''
Input:
- date (YYYY-MM-DD) == ft folder path
'''

import flowtools
import os, sys, datetime

tpl = "INSERT INTO data(stamp, ymd, hour, proto, iip, iport, oip, oport, ibytes, obytes) VALUES (%u, %u, %u, %u, %u, %u, %u, %u, %u, %u);"
netmask	= 4294967040	# 255.255.255.0
hostmask= 255		# 0.0.0.255
net	= 3232235520	# 192.168.0.0/24
TZmete	= 20141026	# > TZ = 1 if stamp > TZmete else 0
TZ1	= 3600
data	= dict()

def	main(argv):
	global data
	root = argv[0]
	stamp = int(root.replace('-', ''))
	# 1. collect data
	for f in os.listdir(root):
		flowset = flowtools.FlowSet(os.path.join(root, f))
		for flow in flowset:
			TZ = TZ1 if (stamp > TZmete) else 0
			dt = datetime.datetime.fromtimestamp(long(flow.last) + TZ)
			ymd, hour = (int(dt.date().isoformat().replace('-', '')), dt.hour)
			proto = flow.prot
			if (flow.dstaddr_raw & netmask) == net:		# inbound
				iip	= flow.dstaddr_raw & hostmask
				iport	= flow.dstport
				oip	= flow.srcaddr_raw
				oport	= flow.srcport
				ibytes	= flow.dOctets
				obytes	= 0
			elif  (flow.srcaddr_raw & netmask) == net:	#outbound
				iip	= flow.srcaddr_raw & hostmask
				iport	= flow.srcport
				oip	= flow.dstaddr_raw
				oport	= flow.dstport
				ibytes	= 0
				obytes	= flow.dOctets
			key = (ymd, hour, proto, iip, iport, oip, oport)
			r = data.get(key, None)
			if r == None:
				data[key] = [ibytes, obytes]
			else:
				data[key] = [r[0]+ibytes, r[1]+obytes]
	# 2. print
	print "BEGIN;"
	print "DELETE FROM data WHERE stamp = %d;" % stamp
	for k, v in data.iteritems():
		print tpl % (stamp, k[0], k[1], k[2], k[3], k[4], k[5], k[6], v[0], v[1])
	print "COMMIT;"

if (__name__ == '__main__'):
	if (len(sys.argv) != 2):
		print 'Usage: %s <folder>' % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1:])
