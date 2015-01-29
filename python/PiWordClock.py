#!/usr/bin/python

import time,os,datetime,sys,getopt,argparse,fonts
from LEDGrid import LEDGrid

def scrollMessage(message,font):
    print (message)

def rotateFontCCW(font,grid=None):
    for c in font:
        font[c]=grid.rotateCCW(font[c])

def demo(message='',font=None,delay=1):
    for m in message:
        grid.showChar(font[m])
        time.sleep(delay)

def merge(words):
    char=[0,0,0,0,0,0,0,0]
    for w in words:
        for x in range(0,8):
            char[x]=char[x] | w[x]
    return char

def demoAllTimes(font=None,grid=None,delay=0.5):
    for m in range(0,720,5):
        tempTime= datetime.datetime.combine(datetime.date.today(),datetime.time(1,0,0))+datetime.timedelta(minutes=m)
        showTime(font,grid,tempTime)
        time.sleep(delay)

def demoQuick(font=None,grid=None,delay=1):
    for m in range(0,720,65):
        tempTime= datetime.datetime.combine(datetime.date.today(),datetime.time(1,0,0))+datetime.timedelta(minutes=m)
        showTime(font,grid,tempTime)
        time.sleep(delay)

def demoTimeList(font=None,grid=None,delay=1,times=[[1,5],[2,10],[3,15],[4,30],[4,35],[5,40],[6,45],[7,50],[8,55],[9,0],[10,5],[11,15],[12,30]]):
    for t in times:
        tempTime= datetime.datetime.combine(datetime.date.today(),datetime.time(t[0],t[1],0))
        showTime(font,grid,tempTime)
        time.sleep(delay)

def showTime(font=None,grid=None,now=datetime.datetime.now()):
    timeString='It is '
    words=[]
    hour=now.hour
    minute=now.minute
    if minute>=5 and minute <10:
        words=['m_5']
    elif minute>=10 and minute <15:
        words=['m_10']
    elif minute>=15 and minute <20:
        words=['m_15']
    elif minute>=20 and minute <25:
        words=['m_20']
    elif minute>=25 and minute <30:
        words=['m_25']
    elif minute>=30 and minute <35:
        words=['m_30']
    elif minute>=35 and minute <40:
        words=['m_25']
    elif minute>=40 and minute <45:
        words=['m_20']
    elif minute>=45 and minute <50:
        words=['m_15']
    elif minute>=50 and minute <55:
        words=['m_10']
    elif minute>=55 and minute <60:
        words=['m_5']
    if minute>=5 and minute<35:
        words.append('past')
    if minute >=35 and minute<60:
        words.append('to')
        hour+=1
    if hour>12:
        hour-=12
    if hour==0:
        hour=12
    words.append('h_'+str(hour))
    #words=['m_20','past','h_10']
    chars=[]
    for w in words:
        chars.append(font[w])
    grid.showChar(merge(chars))
        
print ("Pi Word Clock")
##invader1=(grid.rotateCCW(invader1))

##grid2=LEDGrid(address=0x71,debug=False)
##grid2.showChar(invader1)
##grid2.setBrightness(0)
##demo(['past','to','h_1','h_2','h_3','h_4','h_5','h_6','h_7','h_8','h_9','h_10','h_11','h_12','m_5','m_10','m_15','m_20','m_25','m_30'],clockFont1,0.25)

parser=argparse.ArgumentParser()
parser.add_argument("--demo","-d",help="run through some example times",action="store_true")
parser.add_argument("--address","-a",help="I2C address default is 0x70",default='0x70')
parser.add_argument("--brightness","-b",help="LED brightness (0->15) default is 0",default='0')
args=parser.parse_args()

address=int(args.address,16)
brightness=int(args.brightness,10)
grid=LEDGrid(address=address,debug=False)
grid.setBrightness(brightness)
rotateFontCCW(fonts.clockFont1,grid)
fonts.shapes=grid.rotateFontCCW(fonts.shapes)
#fonts.textFont1=grid.flipFontX(fonts.textFont1)
#fonts.printFont(fonts.textFont1)
#grid.scrollString(textFont1,"{}[]~^|ABCDEFGHIJKLMNOPQRSTUVWXYZ=@<>\"'#?()+*!:\/_-0123456789abcdefghijklmnopqrstuvwxyz",speed=4)


if args.demo:
    print ('demo mode on' )  
    demoAnim=['smile','heart1','heart1F','heart2','heart2F','empty']
    grid.playAnimation(fonts.shapes,demoAnim,speed=0.1)
    grid.scrollString(fonts.shapes,demoAnim,speed=4,spacing=1)
    while True:
        demoTimeList(fonts.clockFont1,grid,1.75)

grid.scrollString(fonts.textFont1," GurgleApps.com Word Clock ",speed=4)    
while True:
    showTime(fonts.clockFont1,grid,datetime.datetime.now())
    
