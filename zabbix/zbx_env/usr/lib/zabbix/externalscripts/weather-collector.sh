#!/bin/bash

if [ ! -f /usr/bin/curl ]; then
    echo "File not found!"
    apt update
    apt -y install curl
fi

/usr/bin/curl http://zabbix-sender/py-cgi/thingspeak.py
/usr/bin/curl http://zabbix-sender/py-cgi/weather.py

