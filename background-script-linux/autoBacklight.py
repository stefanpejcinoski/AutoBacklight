# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cv2
import os
import time
import sys
import numpy as np

b=0

def change_brightness(value):
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
            

def check_prerequisites():
    if(os.path.isfile(os.path.join(os.getcwd(), "stop"))):
        return False
    if("On" not in os.popen("xset -q | grep Monitor | cut -d ' ' -f5").read()):
        return False
    if("disconnected" not in os.popen("xrandr --query | grep HDMI-1").read()):
        return False
    return True

def main():  
    if(check_prerequisites==False):
        sys.exit()    
    camera=cv2.VideoCapture(0)
    if(camera.open(0)==False):
        sys.exit()
    ret, frame=camera.read()
    camera.release()
    avg=np.average(frame)
    value=np.uint32(np.round(avg/2.5-b)) 
    change_brightness(value)
    

if __name__=='__main__':
    main()
