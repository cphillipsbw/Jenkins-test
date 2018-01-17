#!/bin/bash

export TERM=xterm

ip=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

fail=0

function testCode()
{
	code=$1
        config=$2
	number=$3

        echo -e "\033[94m *** Testing $number $code ***\033[0m"
	sudo ngrep -l -d docker0 -qtW byline sip port 6060 > output &
	sleep 2

	echo "sipp -sf $DIR/xml/$config -m 1 -s +$number $ip:6060"
	sipp -sf $DIR/xml/$config -m 1 -s +$number $ip:6060 >> /dev/null

	echo killall ngrep
	sudo killall ngrep

	sleep 2
	cat output
        foundCode=`grep "^SIP/2.0 " output` 

	if [ "`grep \"SIP/2.0 $code \" output`" != "" ]
	then
		message="\033[92m Calling $number with config: $config looking for $code. Found: \n$foundCode\033[0m"
	else
		message="\033[91m Calling $number with config: $config looking for $code. Not found: \n$foundCode\033[0m"
		fail=1
	fi
	echo -e $message
	summary="$summary\n$message"

	echo rm output
	rm output
}

# testCode <expected return code> <xml file> <number to call>
testCode 300 MRD.xml 18436072935
testCode 603 MRD.xml 101289567234
#testCode 650 MRD.xml 19002456234
#testCode 651 MRD.xml 611
#testCode 652 652.xml 13459493100
#testCode 654 MRD.xml 991289567234
testCode 300 MRD.xml 15555551212

echo -e "\nSummary:\n$summary\n\n\033[0m"

sleep 15

exit $fail
