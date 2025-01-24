#!/bin/bash
while true; do
	label=$(date +%Y%m%d-%H%M%S)
    find /home/nas/shared/ -type f -mmin +10 -print | xargs -I{} rm -f "{}"
	echo "$label"
	dd if=/dev/urandom of=/home/nas/shared/$label bs=1M count=1 2>/dev/null
	sleep 1
done
