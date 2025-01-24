> The problem occurs when there are partial outages [..]  Even after the NAS returns, the containers on the server are still in a bad state since the cifs mount doesn't get restarted
> it seems like I need a mechanism to stop the containers (or maybe the whole Compose stack) when the share is unavailable and restart them when it returns

I've actually had this problem on my side. There are power outages over here.
I ended up writing a script like the one you're describing for my needs, it works a lot like what you described.

For now, the docker stacks are hardcoded although it would be possible to pick up the docker stacks that use Samba
and only restart those.



