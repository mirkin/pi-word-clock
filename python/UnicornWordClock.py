#!/usr/bin/python

import UnicornGrid,fonts,time

print ("Pi Word Clock")
grid=UnicornGrid.UnicornGrid()
grid.bg=[0x99,0x00,0x00]
grid.fg=[0x00,0x00,0xff]
demoAnim=['smile','heart1','heart1F','heart2','heart2F','empty']
grid.playAnimation(fonts.shapes,demoAnim,speed=0.1)
grid.scrollString(fonts.textFont1," GurgleApps.com Word Clock ",speed=4)