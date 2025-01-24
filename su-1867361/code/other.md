## Can the watchdog know which container uses what share

The watcher could know which running docker containers are making use of samba shares
and then test which of those are accessible so it can make a decision on whether to stop/start.

See the commands below. Yes it's possible but a bit labour intensive.

```
user@vm2:~/app2$ docker inspect 9a64 | jq '.[].Mounts'
[
  {
    "Type": "volume",
    "Name": "app2_nas-shared",
    "Source": "/var/lib/docker/volumes/app2_nas-shared/_data",
    "Destination": "/home/nas/shared",
    "Driver": "local",
    "Mode": "z",
    "RW": true,
    "Propagation": ""
  }
]
user@vm2:~/app2$ docker volume inspect app2_nas-shared
[
    {
        "CreatedAt": "2025-01-21T03:57:42Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "ac62a5e025b7f8cca6ab33eba240cfbf591496a13122ce26d0def556e025f769",
            "com.docker.compose.project": "app2",
            "com.docker.compose.version": "2.32.4",
            "com.docker.compose.volume": "nas-shared"
        },
        "Mountpoint": "/var/lib/docker/volumes/app2_nas-shared/_data",
        "Name": "app2_nas-shared",
        "Options": {
            "device": "//192.168.1.171/shared",
            "o": "rw,username=guest,password=,uid=1000,gid=1000",
            "type": "cifs"
        },
        "Scope": "local"
    }
]
```

## Verify the actual samba version of mounts

```
cat /proc/mounts | perl -ne 'm/vers=([^,]+),/ && print "$1\n";'
```

## List all shares on a Samba server

```
smbclient -L "//192.168.1.100/" -U guest%
```

## List contents of a specific share on a Samba server

```
smbclient "//192.168.1.100/shared-space" -U guest% -c 'dir'
```

## Notes

Systemd `/etc/fstab` mount options:

  * [x-systemd.requires=network-online.target](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.requires=)
  * [x-systemd.automount](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.automount)
  * [\_netdev](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#_netdev)
  * [x-systemd.device-timeout](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.device-timeout=)
  * [x-systemd.mount-timeout](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.mount-timeout=)
