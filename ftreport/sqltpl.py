#!/bin/env python
# -*- coding: utf-8 -*-
# index: date | inbound | outbound | all
tpl_index = '''
SELECT
	ymd,
	SUM(ibytes)/1024 AS inbound,
	SUM(obytes)/1024 AS outbound,
	(SUM(ibytes)+SUM(obytes))/1024 AS traffic
FROM data
GROUP BY ymd
ORDER BY ymd DESC
'''

# day: for date: ip | inbound | outbound | all
tpl_day_ip = '''
SELECT
	iip,
	SUM(ibytes)/1024 AS inbound,
	SUM(obytes)/1024 AS outbound,
	(SUM(ibytes)+SUM(obytes))/1024 AS traffic
FROM data
WHERE ymd = '%s'
GROUP BY iip
ORDER BY iip ASC
'''

# day: for date: hour | inbound | outbound | all
tpl_day_hour = '''
SELECT
	hour,
	SUM(ibytes)/1024 AS inbound,
	SUM(obytes)/1024 AS outbound,
	(SUM(ibytes)+SUM(obytes))/1024 AS traffic
FROM data
WHERE ymd = '%s'
GROUP BY hour
ORDER BY hour ASC
'''

# day: for date: dport | proto | inbound | outbound | all
# max oport = 49000 (matahari)
tpl_day_oport = '''
SELECT * FROM (
	SELECT
		oport,
		proto,
		SUM(ibytes)/1024 AS inbound,
		SUM(obytes)/1024 AS outbound,
		(SUM(ibytes)+SUM(obytes))/1024 AS traffic
	FROM data
	WHERE ymd = '%s' AND oport < 49001
	GROUP BY oport, proto
	ORDER BY traffic DESC
	LIMIT 50
)
ORDER BY oport, proto
'''

# host: for date+host: proto/srcport | summary | inbound | outbound
tpl_host_srcport = '''
SELECT
	proto,
	iport,
	SUM(ibytes) AS inbound,
	SUM(obytes) AS outbound,
	SUM(ibytes)+SUM(obytes) AS traffic
FROM data
WHERE ymd = '%s' AND iip = %d
GROUP BY proto, iport
ORDER BY traffic DESC
LIMIT 50
'''

# host: for date+host: proto/dstport | summary | inbound | outbound
tpl_host_dstport = '''
SELECT
	proto,
	oport,
	SUM(ibytes) AS inbound,
	SUM(obytes) AS outbound,
	SUM(ibytes)+SUM(obytes) AS traffic
FROM data
WHERE ymd = '%s' AND iip = %d
GROUP BY proto, oport
ORDER BY traffic DESC
LIMIT 50
'''

# host: for date+host+proto+srcport: dstip | summary | in | out
tpl_host_port_dstip = '''
SELECT
	oip,
	SUM(ibytes) AS inbound,
	SUM(obytes) AS outbound,
	SUM(ibytes)+SUM(obytes) AS traffic
FROM data
WHERE ymd = '%s' AND iip = %d AND proto = %d AND %s = %d
GROUP BY oip
ORDER BY traffic DESC
LIMIT 50
'''
