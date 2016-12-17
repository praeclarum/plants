#!/usr/bin/python

import sys
import threading
import spidev
import time
import datetime
import urllib2
import urllib
import RPi.GPIO as GPIO

# From: http://stackoverflow.com/a/16368571/338
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()
            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)
            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

#
# Setup Valve GPIO
#
GPIO.setmode(GPIO.BCM)
VALVE_GPIO = 21
VALVE_ONDUR = 10.0
VALVE_DUTYCYCLE = 0.333
VALVE_STATE = False
VALVE_ONDT = datetime.datetime.now()
GPIO.setup(VALVE_GPIO, GPIO.OUT)
GPIO.output(VALVE_GPIO, VALVE_STATE)

#
# Water the plants when they need it
#

PLANT_AVG_WATER = 4095.0
PLANT_NEEDS_WATER = 3000.0

@setInterval(2.0)
def toggleValve():
  global VALVE_STATE
  global VALVE_ONDT, VALVE_ONDUR, VALVE_DUTYCYCLE
  now = datetime.datetime.now()
  dt = (now - VALVE_ONDT).total_seconds()
  if VALVE_STATE:
    print "IT'S ON", dt
    if dt > VALVE_ONDUR:
      VALVE_STATE = False
  else:
    print "IT'S OFF", dt
    need = PLANT_AVG_WATER <= PLANT_NEEDS_WATER
    print "NEED", need
    if need and dt > VALVE_ONDUR / VALVE_DUTYCYCLE:
      VALVE_STATE = True
      VALVE_ONDT = now
  GPIO.output(VALVE_GPIO, VALVE_STATE)
  #setValve(not VALVE_STATE)
  #print "T=", VALVE_STATE

stopValve = toggleValve()

#
# Setup SPI
#
spi = spidev.SpiDev()
spi.open(0, 0)

print "Plant Waterer 8000"

def logvalue(name, value, tim):
  data = urllib.urlencode({'name':name, 'value':value, 'time': tim})
  r = urllib2.urlopen("http://plants.mecha.parts/data/add", data).read().strip()
  print "%s -> %s" % (data, r)

def readadc12(adcnum):
  if adcnum > 7 or adcnum < 0:
    return -1
  r = spi.xfer2([4 | 2 | (adcnum >> 2), (adcnum & 3) << 6, 0])
  #print "R=", r
  a = ((r[1] & 15) << 8) + r[2]
  return a

lastValveOnTime = time.localtime()
while True:
  # HUMIDITY
  try:
    now = time.localtime()
    t = time.strftime("%Y-%m-%d %H:%M:%S", now)
    print "TIME", t
    for x in range(0, 4):
      value = readadc12(x)
      logvalue("H" + str(x), 4095 - value, t)
      time.sleep(0.5)
    logvalue("V", 1 if VALVE_STATE else 0, t)
  except:
    print "Unexpected error:", sys.exc_info()[0]
    #raise
  time.sleep(5*60)

