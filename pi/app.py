#!/usr/bin/python

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)

print "Plant Waterer 8000"


def readadc12(adcnum):
  if adcnum > 7 or adcnum < 0:
    return -1
  r = spi.xfer2([4 | 2 | (adcnum >> 2), (adcnum & 3) << 6, 0])
  #print "R=", r
  a = ((r[1] & 15) << 8) + r[2]
  return a

while True:
  for x in range(0, 8):
    value = readadc12(x)
    print "V%d=%d" % (x, value)
    time.sleep(0.5)

