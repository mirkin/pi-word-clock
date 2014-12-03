#!/usr/bin/python

import datetime,time
from Adafruit_I2C import Adafruit_I2C

def showChar(c):
  bytes=[]
  for item in c:
    bytes.append( ((item & 0xFE)>>1)|((item & 0x01)<<7) )
    bytes.append(0x00)
    i2c.writeList(0x00,bytes)

def flipX(c):
  result=[0,0,0,0,0,0,0,0]
  for x in range(0,8):
    for y in range(0,8):
      temp=7-x
      result[x]=result[x] | (c[temp] & 0x01<<y) >> 0
  return result

def rotateCCW(c):
  result=[0,0,0,0,0,0,0,0]
  for x in range(0,8):
    for y in range(0,8):
      #print '{0:2d} {1:2d} {2:8b} {3:0=8b}'.format(x,y,c[x],(c[x]&0x01<<y))
      result[x]=result[x] | ( (c[y] & 0x01<<x) >> x <<y)
    print result[x]
  return result

def rotateCW(c):
  result=[0,0,0,0,0,0,0,0]
  for x in range(0,8):
    for y in range(0,8):
      result[x]=result[x] | ( (c[7-y] & 0x01<<x) >> x <<y)
    print result[x]
  return result

print "Pi World Clock"
i2c=Adafruit_I2C(address=0x70)
i2c.write8(0x21,0x00)
i2c.write8(0x81,0x00)
i2c.write8(0xe0 | 0x01,0x00)
smile=[0x3C,0x42,0x95,0xA1,0xA1,0x95,0x42,0x3c]
empty=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
all_on=[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
past=[0x00,0x04,0x04,0x04,0x04,0x00,0x00,0x00]
arrow=[0x18,0x24,0x42,0xff,0x18,0x18,0x18,0x18]
invader1=[0x18,0x3c,0x7e,0xdb,0xff,0x24,0x5a,0xa5]
invader2=[0x18,0x3c,0x7e,0xdb,0xff,0x24,0x5a,0x42]
while True:
  showChar(rotateCCW(invader1))
  time.sleep(0.1)
  showChar(rotateCCW(invader2))
  time.sleep(0.1)
