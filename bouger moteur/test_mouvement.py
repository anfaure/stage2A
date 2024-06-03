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
    angle=180
    harpia.set_sample_mover_velocity(speed)


# Fonction pour déplacer l'échantillon à une position donnée avec une vitesse spécifique
def deplacer_echantillon(position, vitesse):
    # Déplacement de l'échantillon à la position spécifiée
    harpia.sample_mover_go_to_xy_and_wait_stop(position)
    
    # Réglage de la vitesse de déplacement de l'échantillon
    harpia.set_sample_mover_velocity(vitesse)
    

def mouvement(x, y, width, height_divide_by_2):
    for _ in range(height_divide_by_2):
        for _ in range(width):
            x=1+x
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2) # Pour attendre que le mouvement se réalise
        harpia.set_target_rotate_angle(angle)
        y=y+1
        harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
        time.sleep(2) # Pour attendre que le mouvement se réalise
        for _ in range(width):
            x=x-1
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2) # Pour attendre que le mouvement se réalise
        harpia.set_target_rotate_angle(angle)
        y=y+1
        harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
        time.sleep(2) # Pour attendre que le mouvement se réalise

    for _ in range(width):
            x=1+x
            harpia.sampel_mover_go_to_xy_and_wait_stop(x,y)
            time.sleep(2)

# Appel de la fonction pour déplacer l'échantillon
deplacer_echantillon(mouvement, speed)