#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:49:13 2020

@author: stefan
"""



import cv2
import os
import time
import sys
import numpy as np

b=0

        
    
def change_brightness(value):
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
     change_brightness(value)
    

if __name__=='__main__':
    main()
