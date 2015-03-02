import sys
from PyQt4 import QtGui, QtCore
import urllib2 

 
def getdata():
   lista={}
   try:
      page = urllib2.urlopen('http://localhost:5555')
      for dati in page.readlines():   
         chiave,valore=dati.split("|")
         lista[chiave]=valore.rstrip('\n')
   except:
      lista["datetime"]="                                            "
      lista["num_sats"]="Unable to connect!"
   return lista
 
class Main(QtGui.QWidget):
   def __init__(self):
      super(Main, self).__init__()
      self.initUI()
 
   def initUI(self):
      self.timer = QtCore.QTimer(self)
      self.timer.timeout.connect(self.Time)
      self.timer.start(5000)
 
      hbox = QtGui.QHBoxLayout()
      self.tbox = QtGui.QTextEdit()
      self.tbox.setReadOnly(True)
      hbox.addWidget(self.tbox) 
      self.tbox.setText("\n\n\n\n\n\nLoading...")

      vbox = QtGui.QVBoxLayout()
      vbox.addLayout(hbox)
#      vbox.addLayout(hbox2)
#      vbox.addLayout(hbox3)
#      vbox.addLayout(hbox4)

      self.setLayout(vbox)
      self.show()
 
#---------Window settings --------------------------------
         
      self.setGeometry(300,300,240,320)
      self.setWindowTitle("GPS/Meteo info")
 
#-------- Slots ------------------------------------------
 
   def Time(self):
      dati=getdata()
      msg="GPS Date: %s\n" % dati.get("datetime")[:10]
      msg+="GPS Time (UTC): %s\n" % dati.get("datetime")[10:19]
      msg+="LON: %s\n" %dati.get("lon2")
      msg+="LAT: %s\n" %dati.get("lat2")
      msg+="#Sats: %s\n" %dati.get("num_sats")
      msg+="Gps qual: %s\n\n" %dati.get("gps_qual")
      msg+="Heading: %s\n" %dati.get("heading")
      msg+="Speed: %s kn\n\n" %dati.get("lat2")
      msg+="Temp: %s\n" %dati.get("airtemp")
      msg+="Wind speed: %s kn\n" %dati.get("wind_speed")
      msg+="Wind direction: %s\n" %dati.get("wind_dir")
      msg+="Pressure: %s bar\n" %dati.get("pressure")
      msg+="Rel. humidity: %s kn\n" %dati.get("rel_humidity")
      msg+="\n\n\n(c)Rocco De Marco 2015"
      self.tbox.setText(msg)
         
def main():
   app = QtGui.QApplication(sys.argv)
   main = Main()
   sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
