# Docker file for python simple webservice build
FROM ubuntu:16.04

RUN apt-get update && \
    apt-get -y --no-install-recommends install apache2 \
                       python2.7 \
                       python-pip \
    && rm -r /var/lib/apt/lists/*

ADD https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz /opt/

COPY *.py /var/www/html/py-cgi/
COPY 000-default.conf /etc/apache2/sites-available/
COPY apache-foreground /usr/local/bin/

RUN a2enmod cgi && \
    pip install py-zabbix && \
    chmod +x /var/www/html/py-cgi/* \
    && tar zxf /opt/pywapi-0.3.8.tar.gz -C /opt/ && \
    cd /opt/pywapi-0.3.8 && \
    python setup.py build && \
    python setup.py install

EXPOSE 80

CMD [ "apache-foreground" ]

