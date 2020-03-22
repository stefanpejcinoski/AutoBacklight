#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:24:01 2020

@author: stefan
"""

import cv2
import os
import sys
#from subprocess import check_output, CalledProcessError, STDOUT
import numpy as np

"""
def getstatusoutput(cmd):
    try:
        data = check_output(cmd, shell=True, universal_newlines=True, stderr=STDOUT)
        status = 0
    except CalledProcessError as ex:
        data = ex.output
        status = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return status, data
"""
def change_brightness(value):
    os.system('gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 ' + str(value) + '>"')
        

def main():  
    
    if(os.path.isfile('/home/stefan/.autoBacklight/stop')):
        sys.exit()
    camera=cv2.VideoCapture(0)
    if(camera.open(0)==False):
        sys.exit()
    ret, frame=camera.read()
    camera.release()
    avg=np.average(frame)
    change_brightness(np.uint32(np.round(avg/10)))
    

if __name__=='__main__':
    main()
