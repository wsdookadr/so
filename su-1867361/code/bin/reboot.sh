#!/bin/bash
ssh -q -o StrictHostKeyChecking=no -i ~/.ssh/modern root@192.168.1.171 sudo systemctl reboot
ssh -q -o StrictHostKeyChecking=no -i ~/.ssh/modern root@192.168.1.172 sudo systemctl reboot
