#!/usr/bin/python

import datetime,time,unicornhat,Grid

class UnicornGrid(Grid.Grid):

  bg=[0x00,0x00,0x00]
  fg=[0xFF,0xFF,0xFF]

  def __init__(self,debug=False):
    Grid.Grid.__init__(self,debug)
  
  def showChar(self,c):
    for x in range(8):
      for y in range(8):
        if c[y] & 1<<x:
          unicornhat.set_pixel(x,y,self.fg[0],self.fg[1],self.fg[2])
        else:
          unicornhat.set_pixel(x,y,self.bg[0],self.bg[1],self.bg[2])
    unicornhat.show()


  def setBrightness(self,brightness):
    unicornhat.brightness(brightness)

  