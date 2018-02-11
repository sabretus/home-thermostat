# Docker file for python simple webservice build
FROM ubuntu:16.04

RUN apt-get update && \
    apt-get -y install git \
                       python2.7 \
                       python-pip \
		       wget && \
                       mkdir /opt/remiui

ADD remi/* /opt/remiui/

RUN pip install git+https://github.com/dddomodossola/remi.git && \
    pip install py-zabbix && \
    chmod +x /opt/remiui/*

WORKDIR /opt/remiui/

EXPOSE 8082 45607

CMD python /opt/remiui/webui.py

