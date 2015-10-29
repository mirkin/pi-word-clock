#!/usr/bin/python
import time,os,datetime,sys,argparse,fonts,I2CGrid
print ("Eyes (0) (0)")

parser=argparse.ArgumentParser()
parser.add_argument("--addressLeft","-al",help="I2C address left eye default is 0x70",default='0x70')
parser.add_argument("--addressRight","-ar",help="I2C address right eye default is 0x71",default='0x71')
parser.add_argument("--brightness","-b",help="LED brightness (0->15) default is 0",default='0')
args=parser.parse_args()

addressLeft=int(args.addressLeft,16)
addressRight=int(args.addressRight,16)
brightness=int(args.brightness,10)
leftEye=I2CGrid.I2CGrid(address=addressLeft,debug=False)
rightEye=I2CGrid.I2CGrid(address=addressRight,debug=False)
leftEye.setBrightness(brightness)
rightEye.setBrightness(brightness)
fonts.eyes=leftEye.rotateFontCCW(fonts.eyes)
demoAnim=['straight','straightBlink1','straightBlink2','straightBlink3','all_off','straightBlink3','straightBlink2','straightBlink1','straight']
while True:
  leftEye.playAnimation(fonts.eyes,demoAnim,speed=5)
  rightEye.playAnimation(fonts.eyes,demoAnim,speed=5)