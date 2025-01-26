#!/bin/bash
IP="192.168.1.171"
SHARE="/shared"
A=$(cat /proc/mounts | grep /home/nas/shared | wc -l)
B=$(timeout 13 ls /home/nas/shared/ >/dev/null 2>/dev/null ; echo $?)
C=$(timeout 13 smbclient //$IP$SHARE -U guest% -c 'dir' >/dev/null 2>/dev/null; echo $?)
A=$(( !$A ))
C=$(( !$C ))

DC=()
DC+=(/home/user/app)
# echo $(date +"%Y-%m-%d %H:%M:%S")" A=$A B=$B C=$C" >> /home/user/.samba.docker.log

# if Samba server is available
if [[ "$C" -eq "1" ]]; then
	# is Samba share unmounted or unresponsive
	if [ "$A" -ne "0" ] || [ "$B" -ne "0" ]; then
		for s in "${DC[@]}"; do
			sudo -u user bash -c "cd $s; docker compose stop;"
		done
		umount -A --recursive /home/nas/
		mount -a
		for s in "${DC[@]}"; do
			sudo -u user bash -c "cd $s; docker compose up -d;"
		done
	fi
else
	umount -A --recursive /home/nas/
	for s in "${DC[@]}"; do
		sudo -u user bash -c "cd $s; docker compose stop;"
	done
fi


