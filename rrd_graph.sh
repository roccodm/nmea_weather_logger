rrdtool graph mygraph.png -a PNG \
--slope-mode -g -w 180 -h 100 \
--title "Air temperature" \
'DEF:probe1=meteo.rrd:airtemp:AVERAGE' \
'AREA:probe1#00FF00:Air temperature' 

