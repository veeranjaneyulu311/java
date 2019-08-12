#!/bin/sh
export IP=`/sbin/ifconfig eth0 | grep inet | awk '{print $2}'| cut -f2 -d:`
exec gunicorn -w 2 -b $IP:8049 controller:app 
