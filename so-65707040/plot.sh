#!/bin/bash
PROGRAM="$1"
DATA="$2"
OUTPUT="$3"
gnuplot -e "filename='$DATA'; set terminal pngcairo size 800,600 enhanced font 'Segoe UI,10' ; set output '$OUTPUT' ; " -p $PROGRAM
