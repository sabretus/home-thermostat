#!/usr/bin/env python

import pywapi
from pyzabbix import ZabbixMetric, ZabbixSender

print "Content-type: text/html\n\n"

# Lviv
city_code = 'UPXX0017'

# Get data
data = pywapi.get_weather_from_weather_com(city_code, 'metric')

packet = [
    ZabbixMetric('Microserver', 'outside.weather.temp', data['current_conditions']['temperature']),
    ZabbixMetric('Microserver', 'outside.weather.hum', data['current_conditions']['humidity']),
    ZabbixMetric('Microserver', 'outside.weather.wind', data['current_conditions']['wind']['speed']),
    ZabbixMetric('Microserver', 'outside.weather.pressure', data['current_conditions']['barometer']['reading'][:-3])
]

print packet

result = ZabbixSender(use_config=False, zabbix_server='zabbix-server').send(packet)

