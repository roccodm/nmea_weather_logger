# /usr/bin/python -u
# -*- coding: utf-8 -*-

import threading
import time
import signal
import datetime
import serial
import pynmea2
import sqlite3
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
#-----------------------------------------
# Global vars
#-----------------------------------------

running=True
tcport=5555
device="/dev/pts/7"
dataset={}
server = ""

#-----------------------------------------
# General purpose functions
#-----------------------------------------
def exit_nicely(signum, frame):
   global running
   running=False
#   server.socket.close()
   print "Shutting down daemon"
   server.socket.close()
   exit()

# Signal binding
signal.signal(signal.SIGINT, exit_nicely)



#-----------------------------------------
# Thread #1
# poller
#-----------------------------------------


class controller(threading.Thread):
   def __init__(self):
     global dataset
     print "Started thread controller"
     threading.Thread.__init__(self)
     
   def run(self):
     global running
     global device
     global dataset
     try:
        ser=serial.Serial(device,4800,timeout=10)
        while running: 
           data=ser.readline()
           if len(data)>1:
              try:
                 msg=pynmea2.parse(data)
                 if msg.sentence_type=="GGA":
                    dataset["lat"]=msg.latitude
                    dataset["lon"]=msg.longitude
                    dataset["lat2"]=msg.lat[0:2]+' '+msg.lat[2:]+" "+msg.lat_dir
                    dataset["lon2"]=msg.lon[0:3]+' '+msg.lon[3:]+" "+msg.lon_dir
                    dataset["gps_qual"]=msg.gps_qual
                    dataset["num_sats"]=msg.num_sats
                    dataset["altitude"]=msg.altitude
                 if msg.sentence_type=="HDT":
		    dataset["heading"]=msg.heading
                 if msg.sentence_type=="VTG":
		    dataset["navigation_dir"]=msg.true_track
		    dataset["navigation_speed"]=msg.spd_over_grnd_kts
                    dataset["faa_mode"]=msg.faa_mode
                 if msg.sentence_type=="ZDA":
                    dataset["datetime"]=msg.datetime
                 if msg.sentence_type=="MDA":
                    dataset["pressure"]=msg.b_presure_bar
                    dataset["airtemp"]=msg.air_temp
                    dataset["rel_humidity"]=msg.rel_humidity
                    dataset["wind_dir"]=msg.direction_true
                    dataset["wind_speed"]=msg.wind_speed_knots
              except:
		 pass
               #msg=pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D") 
               #msg=pynmea2.parse(data)
      #         print data
     except Exception,e:
        print e


#-----------------------------------------
# Thread module #2
# Insert data into sqlite db
#-----------------------------------------


class database(threading.Thread):
   def __init__(self):
     print "Started thread database"
     threading.Thread.__init__(self)
     
   def run(self):
     global running
     global dataset
     while running:
        if len(dataset)>0:
           conn = sqlite3.connect('meteo.db')
           fields="("
           values="("
           for element in dataset:
              fields+="%s," % element
              values+="'%s'," % dataset[element]
           sql="insert into meteo "+fields[:-1]+") values "+values[:-1]+")"
           conn.execute(sql)
           conn.commit()
           conn.close()
           time.sleep(5)


#-----------------------------------------
# Thread module #3
# webserver
#-----------------------------------------

class myHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      global dataset
      self.send_response(200)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      if len(dataset)>0:
         response=""
         for element in dataset:
            response+="%s:%s\n" % (element,dataset[element])
         self.wfile.write(response)
      else:
         self.wfile.write("response:no data")
      return

   def log_message(self, format, *args):
      return

class webs(threading.Thread):
   def __init__(self):
      print "Started thread webserver"
      threading.Thread.__init__(self)

   def run(self):
      global server
      server = HTTPServer(('', 4775), myHandler)
      server.serve_forever()


controller().start()
database().start()
webs().start()



# Mainloop
while 1:
   time.sleep(1)



"""
Testing:

1) start socat -d -d pty,raw,echo=0 pty,raw,echo=0
2) change the port as the first one of the couple (tipically /dev/pst/9)
3) output sentences to the second one (echo "blabla" > /dev/pts/10)
"""


