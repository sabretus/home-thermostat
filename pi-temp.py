#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import time
from pyzabbix import ZabbixMetric, ZabbixSender
import urllib2

thingspeak_base_url = 'http://api.thingspeak.com/update'
thingspeak_key = ''

base_dir = '/sys/bus/w1/devices/'
# base_dir = './devices/'
circuit_sensor_folder = glob.glob(base_dir + '28-03*')[0]
circuit_sensor_file = circuit_sensor_folder + '/w1_slave'

air_sensor_folder = glob.glob(base_dir + '28-04*')[0]
air_sensor_file = air_sensor_folder + '/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor_file):
    lines = read_temp_raw(sensor_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensor_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

try:
    # Colect sensor values
    air_pi_temp = read_temp(air_sensor_file)
    circuit_pi_temp = read_temp(circuit_sensor_file)

    # Send data to Zabbix
    # print air_pi_temp
    # print circuit_pi_temp
    packet = [ ZabbixMetric('Zabbix server', 'furnance.sensor.one', air_pi_temp),
               ZabbixMetric('Zabbix server', 'furnance.circuit.input', circuit_pi_temp), ]
    result = ZabbixSender(use_config=True).send(packet)

    # Send data to Thingspeak channel
    url = "%s?key=%s&field1=%s&field2=%s" % (thingspeak_base_url,thingspeak_key,air_pi_temp,circuit_pi_temp)
    # print url
    # here is our test comment
    urllib2.urlopen(url).read()

except read_temp.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
