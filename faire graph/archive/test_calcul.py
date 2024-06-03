# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np  # Importation de la bibliothèque NumPy

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I0 - I0bckg) / (I1 - I1bckg)
    delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD


I1=2.23634715E-004
I0=2.13650426E-004
I1bckg=-1.94842976E-003
I0bckg=-1.95080545E-003

# Création liste
liste_delta_OD = []
delta_OD = []
delta_OD.append(calculer_delta_OD(I0, I0bckg,I1, I1bckg))
liste_delta_OD.append(delta_OD)
print(liste_delta_OD[0])