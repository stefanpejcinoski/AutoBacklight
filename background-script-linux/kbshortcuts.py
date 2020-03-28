#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:51:32 2020

@author: stefan
"""

import autobacklight
import os
from time import sleep

def main():
    if (os.path.isfile(os.path.join(os.getcwd(), "stop"))):
        os.remove(os.path.join(os.getcwd(), "stop"))
        os.system('notify-send'+" 'AutoBL'"+' '+"'Service On'")
        sleep(1)
        autobacklight.main()
        
    else:
        open(os.path.join(os.getcwd(), "stop"), "w").close()
        os.system('notify-send'+" 'AutoBL'"+' '+"'Service Off'")
        
        
        
if __name__=='__main__':
    main()