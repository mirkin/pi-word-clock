#!/usr/bin/python
import time,os,datetime,sys,argparse,fonts,I2CGrid,EyeAnimations as ea,threading,json
print ("Eyes (0) (0)")
print len(ea.a)
parser=argparse.ArgumentParser()
parser.add_argument("--addressLeft","-al",help="I2C address left eye default is 0x70",default='0x70')
parser.add_argument("--addressRight","-ar",help="I2C address right eye default is 0x71",default='0x71')
parser.add_argument("--brightness","-b",help="LED brightness (0->15) default is 0",default='15')
args=parser.parse_args()

addressLeft=int(args.addressLeft,16)
addressRight=int(args.addressRight,16)
brightness=int(args.brightness,10)
leftEye=I2CGrid.I2CGrid(address=addressLeft,debug=False)
rightEye=I2CGrid.I2CGrid(address=addressRight,debug=False)
leftEye.setBrightness(brightness)
rightEye.setBrightness(brightness)
fonts.eyes=leftEye.rotateFontCCW(fonts.eyes)

class myThread (threading.Thread):
  def __init__(self, threadID, name, eye, anim):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.eye=eye
      self.anim=anim
  def run(self):
      self.eye.playAnimation(fonts.eyes,self.anim,speed=5)

def loadAnims():
  data={}
  fileName=os.path.dirname(os.path.realpath(__file__))+'/EyeAnimations.json'
  #print os.path.dirname(os.path.realpath(__file__))
  try:
    with open(fileName) as infile:
      data=json.load(infile)
  except EnvironmentError as err:
      print('Oops problem loading JSON! ')
      print (err)
  return data

anims=loadAnims()

while True:
  threadLeft=myThread(1,'left',leftEye,anims['stareAndBlink']['left'])
  threadRight=myThread(2,'right',rightEye,anims['stareAndBlink']['right'])
  threadLeft.start()
  threadRight.start()
  threadLeft.join()
  threadRight.join()
