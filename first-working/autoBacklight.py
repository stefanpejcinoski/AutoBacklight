#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:24:01 2020

@author: stefan
"""

import cv2
import os
import time
import sys
import numpy as np

b=0

def change_brightness_linux(value):
    curValRet=os.popen('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Get org.gnome.SettingsDaemon.Power.Screen Brightness').read()
    curVal=int(''.join(filter(str.isdigit, curValRet))) 
    if (curVal<value):
      inc=1
    elif (curVal>value):
      inc=-1
    else:
      return   
    while True:
      curVal=curVal+inc
      os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 ' + str(curVal) + '>"')
      time.sleep(0.025)
      if(curVal==value):
         break
            
        
    
def change_brightness_windows(value):
    os.system('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,'+value+')')
    

def main():  
    
    if(os.path.isfile(os.path.join(os.getcwd(), "stop"))):
        sys.exit()
    camera=cv2.VideoCapture(0)
    if(camera.open(0)==False):
        sys.exit()
    ret, frame=camera.read()
    camera.release()
    avg=np.average(frame)
    value=np.uint32(np.round(avg/2.5-b))
    if(os.name=='posix'):
        change_brightness_linux(value)
    elif(os.name=='nt'):
        change_brightness_windows(value)
    

if __name__=='__main__':
    main()
