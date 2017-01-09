#!/usr/bin/python

#
# Send data to zabbix using GET request, example:
# sender.py?sensorid=esp8266_001&temp=10&hum=25
#

import cgi
from pyzabbix import ZabbixMetric, ZabbixSender

# Print header
print "Content-type: text/html\n\n"

form = cgi.FieldStorage(keep_blank_values=1)
temp = form.getvalue('temp')
hum = form.getvalue('hum')
sensorid = form.getvalue('sensorid')

print "<h2>Received data:</h2>"

print "Sensor ID: "+sensorid+"<br>"
print "Temperature: "+temp+"C<br>"
print "Humidty: "+hum+"%<br>"

packet = [
	ZabbixMetric('Zabbix server', 'room.sensor.'+sensorid+'.temp', temp),
	ZabbixMetric('Zabbix server', 'room.sensor.'+sensorid+'.hum', hum),
]

print packet

result = ZabbixSender(use_config=True).send(packet)

