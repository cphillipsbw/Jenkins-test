#!/bin/bash

export TERM=xterm

ip=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

touch output

# primer brfore first test
echo " *** Making primary call ***"

while [ "`grep \"^SIP/2.0 300\" output`" == ""  ]
do 
   sudo ngrep -l -d docker0 -qtW byline sip port 6060 > output &
   sleep 30
   sipp -sf $DIR/xml/MRD.xml -m 1 -s +18436072935 $ip:6060 >> output
   sudo killall ngrep
   sleep 2
   echo "`grep \"^SIP/2.0\" output`"
done

cat output
rm output

sleep 30
