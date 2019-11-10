#!/usr/bin/python
import configparser
import re

from pyzabbix import ZabbixAPI


def updatetmp(config_path):
    zabix_server = 'http://zabbix-web-apache-mysql/'
    heatingon_trigger_id = '15435'
    heatingoff_trigger_id = '15436'
    sensor_a = '{Microserver:room.sensor.esp8266_fb539.temp.nodata(5m)}'
    sensor_b = '{Microserver:room.sensor.esp8266_1cc42e.temp.nodata(5m)}'
    zapi = ZabbixAPI(zabix_server, user='api', password='api')

    config = configparser.ConfigParser()
    config.read(config_path)

    temp = config.get('main', 'temp')
    temp_low = float(re.sub('[^0-9.]', '', temp))
    temp_high = float(re.sub('[^0-9.]', '', temp)) + .2

    # print(temp_high)

    timeSlotDayBegin = re.sub(":", "", config.get('main', 'timeSlotDayBegin')) + '00'
    timeSlotDayEnd = re.sub(":", "", config.get('main', 'timeSlotDayEnd')) + '00'
    timeSlotNightBegin = re.sub(":", "", config.get('main', 'timeSlotNightBegin')) + '00'
    timeSlotNightEnd = re.sub(":", "", config.get('main', 'timeSlotNightEnd')) + '00'

    temp_expr = "{Microserver:room.sensor.avg.temp.last()}" + "<" + str(temp_low)
    time_expr = "{Microserver:room.sensor.avg.temp.time()}"

    time_slot_1_expr = time_expr + ">" + timeSlotDayBegin + " and " + time_expr + "<" + timeSlotDayEnd
    time_slot_2_expr = time_expr + ">" + timeSlotNightBegin + " and " + time_expr + "<" + timeSlotNightEnd

    # Zabbix trigger expr: temperature X and time Y or temperature X and time Z
    expr_on = temp_expr + " and " + time_slot_1_expr + " or " + temp_expr + " and " + time_slot_2_expr
    expr_off = '{Microserver:room.sensor.avg.temp.last()}>' + str(round(temp_high, 2)) + ' or ' + sensor_a + '=1 or ' + sensor_b + '=1'

    print(expr_on)
    print(expr_off)

    # Query item's history (integer) data
    result_on = zapi.trigger.update(triggerid=heatingon_trigger_id,
                                    status=0,
                                    description="Heating ON",
                                    expression=expr_on
                                    )

    result_off = zapi.trigger.update(triggerid=heatingoff_trigger_id,
                                     status=0,
                                     description="Heating Off",
                                     expression=expr_off
                                     )
    print(result_on)
    print(result_off)

