#!/usr/bin/python

import datetime,time
from Adafruit_I2C import Adafruit_I2C

class LEDGrid:
  i2c=None

  def __init__(self,address=0x70,debug=False):
    self.i2c=Adafruit_I2C(address=address)
    self.i2c.write8(0x21,0x00)
    self.i2c.write8(0x81,0x00)
    self.i2c.write8(0xe0 | 0x01,0x00)
  
  def showChar(self,c):
    bytes=[]
    for item in c:
      bytes.append( ((item & 0xFE)>>1)|((item & 0x01)<<7) )
      bytes.append(0x00)
      self.i2c.writeList(0x00,bytes)

  def playAnimation(self,font,animation,speed=1):
    delay=0.5**speed
    for frame in animation:
      self.showChar(font[frame])
      time.sleep(delay);


  def scrollString(self,font,message='hello',speed=1,spacing=0):
    delay=0.5 ** speed
    length=len(message)
    charRange=range(length-1)
    for charPos in charRange:
      leftChar=font[message[charPos]]
      rightChar=font[message[charPos+1]]
      for shift in range(8+spacing):
        bytes=[0,0,0,0,0,0,0,0]
        for col in range(8):
          if col>=shift:
            bytes[col]=leftChar[col-shift]
          elif col<shift-spacing:
            bytes[col]=rightChar[col-shift+spacing]
          else:
            bytes[col]=0
        self.showChar(bytes)
        time.sleep(delay)

  def scrollStringOld(self,font,message='hello',speed=1):
    delay=0.5 ** speed
    length=len(message)
    charRange=range(length-1)
    for charPos in charRange:
      leftChar=font[message[charPos]]
      rightChar=font[message[charPos+1]]
      for shift in range(8):
        bytes=[0,0,0,0,0,0,0,0]
        for col in range(8):
          if col>=shift:
            bytes[col]=leftChar[col-shift]
          else:
            bytes[col]=rightChar[col-shift+8]
        self.showChar(bytes)
        time.sleep(delay)

  def scrollStringDown(self,font,message='hello',speed=1):
    delay=0.5 ** speed
    length=len(message)
    charRange=range(length)
    for charPos in charRange:
      leftChar=font[message[charPos]]
      rightChar=font[message[charPos+1]]
      for shift in range(8):
        bytes=[0,0,0,0,0,0,0,0]
        for col in range(8):
          bytes[col]=bytes[col]|leftChar[col]<<shift
          self.showChar(bytes)
        time.sleep(delay)


  def setBrightness(self,brightness):
    self.i2c.write8(0xe0|brightness,0x00)

  def printHex(self,c):
    for x in c:
      print ('0x{0:0=2x}'.format(x))

  @staticmethod
  def flipX(c):
    result=[0,0,0,0,0,0,0,0]
    for x in range(0,8):
      for y in range(0,8):
        temp=7-x
        result[x]=result[x] | (c[temp] & 0x01<<y) >> 0
    return result

  @staticmethod
  def flipFontX(f):
    result=[0,0,0,0,0,0,0,0]
    for l in f:
      f[l]=LEDGrid.flipX(f[l])
    return f

  @staticmethod
  def rotateFontCCW(f):
    result=[0,0,0,0,0,0,0,0]
    for l in f:
      f[l]=LEDGrid.rotateCCW(f[l])
    return f

  @staticmethod
  def rotateCCW(c):
    result=[0,0,0,0,0,0,0,0]
    for x in range(0,8):
      for y in range(0,8):
        #print '{0:2d} {1:2d} {2:8b} {3:0=8b}'.format(x,y,c[x],(c[x]&0x01<<y))
        result[x]=result[x] | ( (c[y] & 0x01<<x) >> x <<y)
    return result

  @staticmethod
  def rotateCW(c):
    result=[0,0,0,0,0,0,0,0]
    for x in range(0,8):
      for y in range(0,8):
        result[x]=result[x] | ( (c[7-y] & 0x01<<x) >> x <<y)
    return result
