#!/bin/bash
#
# Randomly starts/stops the samba server
#
while true; do
  R=$(echo "$(od -An -N4 -tu4 /dev/urandom) % 10 + 1" | bc)
  if [[ "$R" -lt 3 ]]; then
    echo "stopping"
    systemctl stop smbd
  else
    echo "starting"
    systemctl start smbd
  fi
  sleep 2
done
