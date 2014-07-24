set terminal png size 1440,900
set output "/public/www/status/glue_down.png"

set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
set grid xtics lc rgb "#bbbbbb" lw 1 lt 0

set xdata time
set timefmt "%Y-%m-%d"
#set xrange ["2014-03-01":"2014-06-14"]
set xrange [from:to]
set format x "%m-%d"
#set timefmt "%Y-%m-%d %H:%M:%S"

set ytics 0, 1, 24
set xtics from, 604800, to

plot [:][:] "< cat /public/www/status/192.168.0.61-glue_restart.log  | grep down | awk '{print $1,$2}'" using 1:2