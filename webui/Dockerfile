# Docker file for python simple webservice build
FROM python:3

ADD remi/* /opt/remiui/

RUN pip install remi py-zabbix && \
    chmod +x /opt/remiui/*

WORKDIR /opt/remiui/

EXPOSE 8082 45607

CMD python /opt/remiui/webui.py
