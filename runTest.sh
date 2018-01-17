#!/bin/bash

script=$1
docker=$2

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

name=`sudo docker ps | awk '{print $1 " " $2}' | grep $docker | head -n1 | awk '{print $1}'`
ip=`sudo docker inspect $name | grep IPAddress\" | cut -d'"' -f4 | head -n1`

echo IP: $ip
echo $pwd

$DIR/$script $ip
