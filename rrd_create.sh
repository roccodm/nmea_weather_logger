rrdtool create meteo.rrd --start N --step 300 \
DS:airtemp:GAUGE:300:-10:70 \
DS:pressure:GAUGE:300:0:2 \
DS:windspeed:GAUGE:300:0:150 \
DS:winddir:GAUGE:300:-360:360 \
DS:humidity:GAUGE:300:0:100 \
RRA:MIN:0.5:12:1440 \
RRA:MAX:0.5:12:1440 \
RRA:AVERAGE:0.5:1:1440
