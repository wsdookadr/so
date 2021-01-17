#!/bin/bash
# ~ 1h to run
PROGRAM="$1"
START="$2"
END="$3"
for i in $(seq $START $END); do
    >&2 echo "Running for input $i"
    a=$(/usr/bin/time -f %e,%M python3 $PROGRAM $i 2>&1 >/dev/null)
    echo "$i,$a"
done
