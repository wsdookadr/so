> The problem occurs when there are partial outages [..]  Even after the NAS returns, the containers
> on the server are still in a bad state since the cifs mount doesn't get restarted [..]
> it seems like I need a mechanism to stop the containers (or maybe the
whole Compose stack) when the share is unavailable and restart them when
it returns

I've actually had this problem on my side. There are power outages over here.

I ended up writing a script like the one you're describing for my needs, it works a lot like what you described.

I had to write some provisioning via Terraform, Ansible and Proxmox to
test it thoroughly. There were two scenarios tested:

- samba share gets mounted on the host and then mounted onto the docker container
- samba share gets directly mounted into docker compose

Even though I was recommended to use the latter, I noticed the former works better.

For now, the docker stacks are hardcoded although it would be possible
to pick up the right docker stack paths automatically (the ones that make use of Samba shares).

[code](https://github.com/wsdookadr/so/tree/master/su-1867361)
