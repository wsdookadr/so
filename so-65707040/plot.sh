#!/bin/bash
DATA="$1"
OUTPUT="$2"
gnuplot -e "filename='$DATA'; set terminal pngcairo size 800,600 enhanced font 'Segoe UI,10' ; set output '$OUTPUT' ; " -p plot.gnuplot
