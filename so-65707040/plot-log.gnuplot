set datafile separator ','
set key autotitle columnhead
set ylabel "log(Time) (seconds)" 
set xlabel 'log(N) (matrix size)'
set y2tics
set ytics nomirror
set y2label "log(Memory) (KB)" 
set style line 100 lt 1 lc rgb "grey" lw 0.5 
set grid ls 100 
set ytics
set xtics
set xtics rotate

set logscale x 2
set logscale y 2
set logscale y2 2

set style line 101 lw 3 lt rgb "#26dfd0"
set style line 102 lw 4 lt rgb "#b8ee30"

plot filename using 1:2 with lines ls 101 axis x1y1, '' using 1:3 with lines ls 102 axis x1y2, ''

