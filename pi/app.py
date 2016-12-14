#!/usr/bin/python

import sys
import spidev
import time
import urllib2
import urllib

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

while True:
  # HUMIDITY
  try:
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "TIME", t
    for x in range(0, 4):
      value = readadc12(x)
      logvalue("H" + str(x), 4095 - value, t)
      time.sleep(0.5)
  except:
    print "Unexpected error:", sys.exc_info()[0]
    #raise
  time.sleep(60)

