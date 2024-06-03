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
    harpia = Harpia('127.0.0.1')

# Check if connection successful
    if not harpia.connected:
        sys.exit("Could not connect to Harpia")

#aller au point 0
    harpia.sample_mover_go_to_zero() 

#lire position x
    harpia.sample_mover_actual_position_x()
#pas bien écrit trouver la bonne tournure 

#aller au point x et y
harpia.sample_mover_go_to_xy_and_wait_for_stop(2,0)
#faire executé le script "a_tester" pour vérifier la bonne tournure de la demande