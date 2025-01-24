#!/bin/bash
# 
# Monitors samba share availability and starts/stops docker stack depending on that.
#
DIR="/home/user/app"
while true; do
        x=`smbclient //192.168.1.171/shared -U guest% -c 'dir' >/dev/null 2>/dev/null; echo $?;`
        echo "x=$x"
        if [[ "$x" == "0" ]]; then
                cd $DIR
                echo "start"
                docker compose up -d
        else
                cd $DIR
                echo "stop"
                docker compose stop
        fi
        sleep 2
done
