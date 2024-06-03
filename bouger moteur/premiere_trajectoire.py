#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Script de contrôle du moteur
#--------------------------------------------------------------------------
# Ce script démontre le contrôle d'un moteur avec des axes X et Y
#==========================================================================
import time
import sys

from lightcon.harpia import Harpia

if __name__ == "__main__":
# initialize connection to Harpia 
    harpia = Harpia('129.20.76.21')

# Check if connection successful
    if not harpia.connected:
        sys.exit("Could not connect to Harpia")
    
#aller au point 0
    harpia.sample_mover_go_to_zero() 
    x=0
    y=0
    for _ in range(1):
        y+=1
        for _ in range(1):
            x+=1
#aller au point x et y
            harpia.sample_mover_go_to_xy_and_wait_for_stop(x,y)

#lire position x
        harpia.sample_mover_actual_position_x()

#lire position y
        harpia.sample_mover_actual_position_y()