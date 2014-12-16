#!/usr/bin/python

import time,os,datetime,sys,getopt,argparse
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
    words=[]
    hour=now.hour
    minute=now.minute
    if minute>=5 and minute <10:
        words=['m_5','past']
    elif minute>=10 and minute <15:
        words=['m_10','past']
    elif minute>=15 and minute <20:
        words=['m_15','past']
    elif minute>=20 and minute <25:
        words=['m_20','past']
    elif minute>=25 and minute <30:
        words=['m_25','past']
    elif minute>=30 and minute <35:
        words=['m_30','past']
    elif minute>=35 and minute <40:
        hour+=1
        words=['m_25','to']
    elif minute>=40 and minute <45:
        hour+=1
        words=['m_20','to']
    elif minute>=45 and minute <50:
        hour+=1
        words=['m_15','to']
    elif minute>=50 and minute <55:
        hour+=1
        words=['m_10','to']
    elif minute>=55 and minute <60:
        hour+=1
        words=['m_5','to']
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
smile=[0x3C,0x42,0x95,0xA1,0xA1,0x95,0x42,0x3c]
empty=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
all_on=[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
past=[0x00,0x00,0x1e,0x00,0x00,0x00,0x00,0x00]
arrow=[0x18,0x24,0x42,0xff,0x18,0x18,0x18,0x18]
invader1=[0x18,0x3c,0x7e,0xdb,0xff,0x24,0x5a,0xa5]
invader2=[0x18,0x3c,0x7e,0xdb,0xff,0x24,0x5a,0x42]
##invader1=(grid.rotateCCW(invader1))

##clockfont1 template
##HATWENTY
##FIFVTEEN
##LF*PASTO
##NINEEIGHT
##ONETHREE
##TWELEVEN
##FOURFIVE
##SIXSEVEN
clockFont1={
    'past':[0x00,0x00,0x1e,0x00,0x00,0x00,0x00,0x00],
    'to':[0x00,0x00,0x03,0x00,0x00,0x00,0x00,0x00],
    'h_1':[0x00,0x00,0x00,0x00,0xe0,0x00,0x00,0x00],
    'h_2':[0x00,0x00,0x00,0x00,0x00,0xc0,0x40,0x00],
    'h_3':[0x00,0x00,0x00,0x00,0x1f,0x00,0x00,0x00],
    'h_4':[0x00,0x00,0x00,0x00,0x00,0x00,0xf0,0x00],
    'h_5':[0x00,0x00,0x00,0x00,0x00,0x00,0x0f,0x00],
    'h_6':[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xe0],
    'h_7':[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1f],
    'h_8':[0x00,0x00,0x00,0x1f,0x00,0x00,0x00,0x00],
    'h_9':[0x00,0x00,0x00,0xf0,0x00,0x00,0x00,0x00],
    'h_10':[0x00,0x00,0x00,0x01,0x01,0x01,0x00,0x00],
    'h_11':[0x00,0x00,0x00,0x00,0x00,0x3f,0x00,0x00],
    'h_12':[0x00,0x00,0x00,0x00,0x00,0xf6,0x00,0x00],
    'm_5':[0x00,0xd4,0x00,0x00,0x00,0x00,0x00,0x00],
    'm_10':[0x00,0x0d,0x00,0x00,0x00,0x00,0x00,0x00],
    'm_15':[0x00,0xef,0x00,0x00,0x00,0x00,0x00,0x00],
    'm_20':[0x3f,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    'm_25':[0x3f,0xd4,0x00,0x00,0x00,0x00,0x00,0x00],
    'm_30':[0xc0,0x00,0xc0,0x00,0x00,0x00,0x00,0x00]
            }
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
rotateFontCCW(clockFont1,grid)

if args.demo:
    print ('demo mode on' )  
    while True:
        demoTimeList(clockFont1,grid,1.75)
        
while True:
    ##showTime(clockFont1,grid2,datetime.datetime.now())
    showTime(clockFont1,grid,datetime.datetime.now())
    
