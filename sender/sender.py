#!/usr/bin/python

#
# Send data to zabbix using GET request, example:
# sender.py?sensorid=esp8266_001&temp=10&hum=25
#
import sys
import cgi
from pyzabbix import ZabbixMetric, ZabbixSender

# Print header
print "Content-type: text/html\n\n"

form = cgi.FieldStorage(keep_blank_values=1)
temp = form.getvalue('temp')
hum = form.getvalue('hum')
sensorid = form.getvalue('sensorid')

# Furnace sensor pass ID via Humidty value (there are no Humidty sensors)
if (sensorid == 'furnace' and hum == '1.00'):
	sensorid = 'furnace.1'
elif (sensorid == 'furnace' and hum == '0.00'):
	sensorid = 'furnace.0'

if temp == 'nan':
    sys.exit()

print "<h2>Received data:</h2>"
print "Sensor ID: "+sensorid+"<br>"
print "Temperature: "+temp+"C<br>"
print "Humidty: "+hum+"%<br>"

packet = [
	ZabbixMetric('Microserver', 'room.sensor.'+sensorid+'.temp', temp),
	ZabbixMetric('Microserver', 'room.sensor.'+sensorid+'.hum', hum),
]

print packet

result = ZabbixSender(use_config=False, zabbix_server='zabbix-server').send(packet)

print result
