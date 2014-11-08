= Stages =
* ./ft2sql.py YYYY-MM-DD>data.sql	43"
* sqlite3 data.db<data.sql	30"
or
* ./ft2sql.py YYYY-MM-DD | sqlite3 data.db	1'45"

= Reports =
* Index: day > in/out
* Daily: day = hour > in/out; day = host > in/out
* Hourly: day+hour = host > in/out
* Hostly: day+host[+hour] = proto/dstport > dstip
* srcport, dstport

= Filter =
* Date (YY-MM-DD)
* > Hour
* proto
* iip
* iport
* oip
* oport
Result:
* [hour]
* iip
* iport
* oip
* oport
* ibytes
* obytes
* bytes

= DB =
ymd:	uint_16 (from last)
h:	uint_8 (from last)
proto:	uint_8
iip:	uint_8 (last octet)
iport:	uint_16
oip:	uint_32
oport:	uint_16
ibytes:	uint_32
obytes:	uint_32
====
SUM:	21 bytes

framework:
web (python-webpy) - http://webpy.org/
flowtools (pyflowtools.rpm)

= Speedup =
* :memory

= TODO =
date: group by p,oport
chkdate: check date and h ranges; date: mintime, maxtime, traffic
mk auto TZ:
	- store mintime/maxtime
	- store date and h as is
	- before print define real TZ: 2014-10-30 22:59:09 .. 2014-10-31 22:59:02 => TZ=+1H (stderr)
	- during print tune date and h
add snap:int (yyyymmdd)
view
