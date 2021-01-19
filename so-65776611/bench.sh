#!/bin/bash
PROGRAM="$1"
TYPE="$2"
START="$3"
STEP="$4"
END="$5"

echo "N,time"
for i in $(seq $START $STEP $END); do
    >&2 echo "Running for input $i"
    a=$(python3 $PROGRAM --type $TYPE --size $i)
    echo "$i,$a"
done


