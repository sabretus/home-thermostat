#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
from ConfigParser import SafeConfigParser
import re

def updatetmp(config_path):
    zabix_server = 'http://localhost/zabbix'
    heatingon_trigger_id = '13563'
    heatingoff_trigger_id = '13564'
    zapi = ZabbixAPI(zabix_server, user='', password='')

    config = SafeConfigParser()
    config.read(config_path)

    temp = re.sub("\D", "", config.get('main', 'temp'))
    timeSlotDayBegin = re.sub(":", "", config.get('main', 'timeSlotDayBegin')) + '00'
    timeSlotDayEnd = re.sub(":", "", config.get('main', 'timeSlotDayEnd')) + '00'
    timeSlotNightBegin = re.sub(":", "", config.get('main', 'timeSlotNightBegin')) + '00'
    timeSlotNightEnd = re.sub(":", "", config.get('main', 'timeSlotNightEnd')) + '00'

    temp_expr = "{Zabbix server:room.sensor.avg.temp.last()}" + "<" + temp
    time_expr = "{Zabbix server:room.sensor.avg.temp.time()}"

    time_slot_1_expr = time_expr + ">" + timeSlotDayBegin + " and " + time_expr + "<" + timeSlotDayEnd
    time_slot_2_expr = time_expr + ">" + timeSlotNightBegin + " and " + time_expr + "<" + timeSlotNightEnd

    # Zabbix trigger expr: temperature X and time Y or temperature X and time Z
    expr_on = temp_expr + " and " + time_slot_1_expr + " or " + temp_expr + " and " + time_slot_2_expr
    expr_off = '{Zabbix server:room.sensor.avg.temp.last()}>' + temp + '.2 or {Zabbix server:room.sensor.esp8266_001.temp.nodata(5m)}=1 or {Zabbix server:room.sensor.esp8266_002.temp.nodata(5m)}=1'

    # print expr_on

    # Query item's history (integer) data
    result = zapi.trigger.update(triggerid=heatingon_trigger_id,
                                 status=0,
                                 description="Heating ON",
                                 expression=expr_on
                                )

    result = zapi.trigger.update(triggerid=heatingoff_trigger_id,
                                 status=0,
                                 description="Heating Off",
                                 expression=expr_off
                                )
