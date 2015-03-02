#!/usr/bin/python
import urllib2
page = urllib2.urlopen('http://localhost:5555')
lista={}
for dati in page.readlines():
   try:
      chiave,valore=dati.split("|")
      lista[chiave]=valore.rstrip('\n')
   except:
      pass

