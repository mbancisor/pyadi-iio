#!/bin/bash
master_IP="192.168.1.60"
slave_IP="192.168.1.61"
export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/site-packages

for i in {1..1000000}
do

	echo "Welcome $i times"

	python adrv9009_som_multi.py 50
	echo "Powering OFF"
	sshpass -p 'analog' ssh root@192.168.1.60 poweroff
	sshpass -p 'analog' ssh root@192.168.1.61 poweroff
	sleep 4
	echo "Power OFF"	
	python __init__.py 192.168.1.102 1 off
	python __init__.py 192.168.1.102 2 off
	python __init__.py 192.168.1.102 3 off
	sleep 6	
	echo "Power ON"
	python __init__.py 192.168.1.102 1 on
	python __init__.py 192.168.1.102 2 on
	python __init__.py 192.168.1.102 3 on

	sleep 55

done


#        sshpass -p 'analog' ssh root@$master_IP 'bash -s' < ./unsync.sh
#        sshpass -p 'analog' ssh root@$slave_IP 'bash -s' < ./unsync.sh
#        echo unsync done
#        sleep 0.1

