#!/bin/bash
# ~ 1h to run
seq 2 42 | xargs -I{} bash -c 'a=$(/usr/bin/time -f %e,%M python3 measure.py {} 2>&1) ; echo "{},$a"'
