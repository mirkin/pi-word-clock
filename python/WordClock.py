#!/usr/bin/python
import datetime

class WordClock:

  myGrid=None

  def __init__(self,grid):
    print('WordClick init:')
    self.myGrid=grid

  def showTime(self,font=None,now=datetime.datetime.now()):
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
    self.myGrid.showChar(self.merge(chars))

  def merge(self,words):
    char=[0,0,0,0,0,0,0,0]
    for w in words:
        for x in range(0,8):
            char[x]=char[x] | w[x]
    return char

  def rotateFontCCW(self,font):
    for c in font:
        font[c]=self.myGrid.rotateCCW(font[c])

