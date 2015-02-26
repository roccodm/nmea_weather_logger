#!/usr/bin/python -u

# Semplice player che riproduce una riga ogni 0.5 secondi
# il file di input va indicato come parametro

import sys
import time

file=open(sys.argv[1])

for riga in file.readlines():
   print riga,
   time.sleep(0.1)
