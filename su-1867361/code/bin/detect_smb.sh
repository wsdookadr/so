#!/bin/bash
#
# Usage:
#
# ./bin/detect_smb.sh
#
# Description:
#
# Shows open ports and supported SMB versions for a particular public share on a Samba server.
#
# References:
#
# https://wiki.samba.org/index.php/SMB3_kernel_status
# https://manpages.debian.org/testing/cifs-utils/mount.cifs.8.en.html
# https://www.nakivo.com/blog/cifs-vs-smb/
# https://wiki.sharewiz.net/doku.php?id=ubuntu:samba:smb_protocol_versions
# https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/storage_administration_guide/mounting_an_smb_share#supported_smb_protocol_versions
# https://www.qnap.com/en/how-to/tutorial/article/how-to-use-smb-3-0-in-qts-4-2
#

IP="192.168.1.171"
SHARE="/shared"

#IP="192.168.1.100"
#SHARE="/shared-space"

echo "IP=$IP SHARE=$SHARE"

for p in 137 138 139 445; do
  timeout 0.2 nc -z $IP $p >/dev/null 2>/dev/null
  if [[ "$?" -eq "0" ]]; then
    s="YES"
  else
    s="NO"
  fi
  printf "PORT=%-7s%s\n" "$p" "$s"
done

for v in 1 1.0 2.0 2.1 2.22 2.24 3 3.0 3.01 3.02 3.20 3.1 3.1.1 3.2 3.10 3.11 3.12 4.0 4.20; do
  s="x"
  umount $v 2>/dev/null
  mkdir $v 2>/dev/null
  mount -t cifs -o "rw,vers=$v,user=guest,password=" //$IP$SHARE `pwd`/$v/ 2>/dev/null >/dev/null
  if [[ "$?" -eq "0" ]]; then
    s="YES"
  else
    s="NO"
  fi
  umount $v 2>/dev/null
  rm -rf "$v"
  printf "VERS=%-7s%s\n" "$v" "$s"
done

