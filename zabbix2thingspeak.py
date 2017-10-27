#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://github.com/adubkov/py-zabbix

from pyzabbix import ZabbixAPI
import urllib2

thingspeak_base_url = 'http://api.thingspeak.com/update'
thingspeak_key = ''
zabix_server = 'http://localhost/zabbix'

zapi = ZabbixAPI(zabix_server, user='', password='')
item_ids = ['23842', '23727']
temp = []

# Query item's history (integer) data
history = zapi.history.get(itemids=item_ids,
                           output='extend',
                           limit='2',
                           history=0,
                           sortfield='clock',
                           sortorder='DESC',
                           )

for point in history:
    # print("{0}".format(point['value']))
    temp.append(point['value'])

# Form url, field1 = air, field2 = water circuit
url = "%s?key=%s&field1=%s&field2=%s" % (thingspeak_base_url,thingspeak_key,temp[0],temp[1])
# Send data to Thingspeak channel
urllib2.urlopen(url).read()
