#!/bin/bash
ssh root@node5 qm list | grep " vm[12] " | awk '{print $1}' | xargs -I{} ssh root@node5 qm stop {}
