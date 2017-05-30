#!/usr/bin/python

import sys
import threading
import spidev
import time
import datetime
import urllib2
import urllib
import json
import RPi.GPIO as GPIO
import math

sys.path.insert(0, '../cat')
import blocks

#
# Pins
#

VALVE_RELAY_GPIO = 36 # K1 Green
SENSOR_RELAY_GPIO = 37 #// K2 Blue
FAN_RELAY_GPIO = 29 #// K3 Yellow
LIGHT_RELAY_GPIO = 31 #// K4 Orange

VALVE_RELAY = 0 
SENSOR_RELAY = 0 
FAN_RELAY = 1 
LIGHT_RELAY = 1 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(VALVE_RELAY_GPIO, GPIO.OUT)
GPIO.setup(SENSOR_RELAY_GPIO, GPIO.OUT)
GPIO.setup(FAN_RELAY_GPIO, GPIO.OUT)
GPIO.setup(LIGHT_RELAY_GPIO, GPIO.OUT)

def output():
  GPIO.output(VALVE_RELAY_GPIO, VALVE_RELAY)
  GPIO.output(SENSOR_RELAY_GPIO, SENSOR_RELAY)
  GPIO.output(FAN_RELAY_GPIO, FAN_RELAY)
  GPIO.output(LIGHT_RELAY_GPIO, LIGHT_RELAY)



#
# Setup SPI
#
spi = spidev.SpiDev()
spi.open(0, 0)

print "Plant Waterer 10000"

def readadc12(adcnum):
  r = spi.xfer2([4 | 2 | (adcnum >> 2), (adcnum & 3) << 6, 0])
  #print "R=", r
  a = ((r[1] & 15) << 8) + r[2]
  return a

def gettemp(analog):
  ratio = analog / 4095.0 #R1/(R1+R2)=ratio
  r2 = 10000
  r1 = r2/(1 - ratio) - r2
  #print "ratio=", ratio, "R1=",r1
  r = r1
  K = 273.15
  t0 = 25 + K
  t1 = 30 + K
  r0 = 10000
  r1 = 8034
  B = (math.log(r1) - math.log(r0)) / (1/t1 - 1/t0)
  #print "B=",B
  ti = 1/t0 + 1/B * math.log(r / r0)
  degC = 1/ti - K
  degF = 9.0/5.0*degC + 32.0
  #print "Deg F=",degF
  return degF

class Plants(blocks.Application):
  def __init__(self):
    super(Plants,self).__init__("plants")
    self.camera_directory = "/home/pi/weed/cat/static"
  def run(self):
    a = gettemp(readadc12(3))
    print "Temperature=", a, " F"

    yield 3.0

blocks.start(Plants(), debug_web = False)

