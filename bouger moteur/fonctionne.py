import time
import sys
from lightcon.harpia import Harpia

if __name__=="__main__":
    harpia = Harpia('127.0.0.1')
    if not harpia.connected:
        sys.exit("Could not connect to Harpia")
    harpia.chopper_start()
    harpia.sampel_mover_go_to_zerro()
    x=0
    y=0
    # Demander à l'utilisateur les paramètres
    height = float(input("Entrez la hauteur : "))
    width=float(input("Entrez la largeur : "))
    speed=float(input("Entrez la vitesse : "))
    height_divide_by_2=height/2

    for _ in range(height_divide_by_2):
        for _ in range(width):
            x=1+x
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2)
        y=y+1
        harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
        time.sleep(2)
        for _ in range(width):
            x=x-1
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2)
        y=y+1
        harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
        time.sleep(2)

    for _ in range(width):
            x=1+x
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2)
