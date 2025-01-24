## Goal

Some experiments on how Samba shares mounted on host or directly into docker affect the containers once the Samba server becomes unavailable.

## Overview

There will be two VMs, one acting as the Samba server and another as Samba client.

## Initial setup

```
terraform init -upgrade
terraform apply -auto-approve
ansible-playbook -i inventory main.yml
```

```
terraform destroy
```

## Scenario 1: Slow NAS boot time

```
ansible-playbook -i inventory p/1.yml
reboot.sh
```

The base Debian 12 boot-time is 39.5s (as reported by `systemd-analyze time`) on my machine.

A delay is injected to prevent samba from starting in a reasonable amount of time on `A`.
Then the two machines are rebooted for the changes to take effect.

Note: The delay may need to be adjusted to fit your hardware.

The samba mount in fstab will fail to mount as can be seen in the systemd logs:

```
root@vm2:~# journalctl -x --since "40 minutes ago" | grep "Failed to mount"
Jan 20 23:51:05 vm2 systemd[1]: Failed to mount home-nas-shared.mount - /home/nas/shared.
```

## Scenario 2: Docker app writes to a samba share mounted on the host but it breaks mid-operation

```
ansible-playbook -i inventory p/2.yml
```

`B` has the samba share mounted, which is then further mounted into a container.
In the container there's an app that writes to the samba mount.

Mid-operation the samba server on `A` is killed but the docker container keeps writing to the same location.

It has nondeterministic behavior:
- sometimes it hangs on writes
- other times it actually writes to `B`'s storage because `A` is down.p

## Scenario 3: Docker compose mounts its own samba share

Same as before but this time docker mounts the samba share to the container.

```
ansible-playbook -i inventory p/3.yml
```

Just as before, it hangs on writes, but this time the container can't even be stopped, it just hangs indefinitely.

## Reset

Restore all state to how it was after running `main.yml`

```
ansible-playbook -i inventory p/reset.yml
```

## Other

The inventory has a variable called `smb_vers` . The most common values for this are `2.0` , `3.0`, `3.11`.

To get a full list of SMB versions supported run the following script:

```
user@perm1:~/code/tf/samba-tests$ sudo ./bin/detect_smb.sh 
[sudo] password for user: 
IP=192.168.1.171 SHARE=/shared
PORT=137    NO
PORT=138    NO
PORT=139    YES
PORT=445    YES
VERS=1      NO
VERS=1.0    NO
VERS=2.0    YES
VERS=2.1    YES
VERS=2.22   NO
VERS=2.24   NO
VERS=3      YES
VERS=3.0    YES
VERS=3.01   NO
VERS=3.02   YES
VERS=3.20   NO
VERS=3.1    NO
VERS=3.1.1  YES
VERS=3.2    NO
VERS=3.10   NO
VERS=3.11   YES
VERS=3.12   NO
VERS=4.0    NO
VERS=4.20   NO
```

The docker compose setup won't seven start for `vers=2.0`, you need at least `3.0`.

These tests cannot be performed over LXC containers, because they don't support mounting network shares so VMs are required.

## Places where people are discussing this problem

- https://superuser.com/q/1867361/2052741

## Versions used

| name      | version         |
|-----------|-----------------|
| debian    | 12              |
| smbd      | 4.17.12-Debian  |
| docker    | 27.5.0          |
| systemd   | 252             |
| terraform | v1.10.3         |
| ansible   | 2.14.16         |