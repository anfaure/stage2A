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

    harpia.sampel_mover_set_position()
#    harpia.sampel_mover_set_position_x()
#    harpia.sampel_mover_set_positionx()
#    harpia.sample_mover_actual_position()
#    harpia.sample_mover_set_position_X()
#    harpia.sample_mover_set_relative_position_X()
#    harpia.sample_mover_position_X(self)
#    harpia.sample_mover_set_sample_stage_position_X()