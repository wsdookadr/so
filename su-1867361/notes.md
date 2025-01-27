> The problem occurs when there are partial outages [..]  Even after the NAS returns, the containers
> on the server are still in a bad state since the cifs mount doesn't get restarted [..]
> it seems like I need a mechanism to stop the containers (or maybe the
whole Compose stack) when the share is unavailable and restart them when
it returns

I've actually had this problem on my side. There are power outages over here.

I ended up [writing a script](https://github.com/wsdookadr/so/blob/master/su-1867361/code/templates/samba-docker-fix.sh)
like the one you're describing for my needs, it works a lot like what you described. It then gets scheduled to run
periodically as a [systemd timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html).

I had to write some provisioning via Terraform, Ansible and Proxmox to
test it thoroughly. I've tested a few scenarios:

- samba share gets mounted on the host and then mounted onto the docker container
- samba share gets directly mounted into docker compose
- long boot-times for the NAS

Even though I was recommended to mount the Samba share directly onto the container, I've noticed it's actually
more practical to mount it on the host (because mounting directly onto the container won't allow me to stop the container
when the mount point is frozen).

For now, the docker stacks are hardcoded although it would be possible
to pick up the right docker stack paths automatically (the ones that make use of Samba shares).

About long boot-times for the NAS I've tried some systemd fstab options such as  [x-systemd.device-timeout](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.device-timeout=) and [x-systemd.mount-timeout](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#x-systemd.mount-timeout=), neither of which worked as advertised in their respective documentations.

[code](https://github.com/wsdookadr/so/tree/master/su-1867361)


UPDATE 2025-01-27:

Possible future improvements:
- automatically detect samba-using docker containers and only consider those (instead of using hardcoded paths as the code works now)
- automatically cross-reference docker containers to the samba shares they use so only those samba shares will be remounted
- measure bandwidth on the tcp samba ports to determine if the samba shares are actively being used or in fact, frozen


