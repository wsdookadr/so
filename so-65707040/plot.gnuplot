set datafile separator ','
set key autotitle columnhead
set ylabel "Time (seconds)" 
set xlabel 'N (matrix size)'
set y2tics
set ytics nomirror
set y2label "Memory (KB)" 
set style line 100 lt 1 lc rgb "grey" lw 0.5 
set grid ls 100 
set ytics
set xtics 1 

set xtics rotate

set style line 101 lw 3 lt rgb "#26dfd0" # style for measuredValue (2) (light blue)
set style line 102 lw 4 lt rgb "#b8ee30" # style for secondYAxisValue (3) (limegreen)

plot filename using 1:2 with lines ls 101 axis x1y1, '' using 1:3 with lines ls 102 axis x1y2, ''

