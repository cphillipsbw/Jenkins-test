#!/bin/bash


name=`sudo docker ps | grep master | awk '{print $1}'`
ip=`sudo docker inspect $name | grep IPAddress\" | cut -d'"' -f4 | head -n1`

echo "Master: $name  IP: $ip"
sed -i "s/ip = .*/ip = $ip/g" lcrnode/etc/environment.conf

