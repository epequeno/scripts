#!/bin/bash

if [ $1 == 'eth0' ]; then
	ip a | egrep "eth0$" | awk '{print $2}' | awk -F"/" '{print $1}'
elif [ $1 == "eth0:0" ]; then
	ip a | egrep "eth0:0$" | awk '{print $2}' | awk -F"/" '{print $1}'
else
	echo "invalid public IP" >2 script.log
fi
