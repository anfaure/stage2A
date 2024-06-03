file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np  # Importation de la bibliothèque NumPy

# Lecture des données
with open(file_path, 'r') as f:
    I1 = []
    for _ in range(12):  # Ignorer les 14 premières lignes
        next(f)
    quinzieme_ligne = next(f)  # Lecture de la quinzième ligne
    data = quinzieme_ligne.split()  # Séparation de la quinzième ligne en une liste de chaînes de caractères
    I1.append(data)  # Ajout de la quinzième colonne à la liste I0
    I0 = []
    for _ in range(14):  # Ignorer les 14 premières lignes
        next(f)
    quinzieme_ligne = next(f)  # Lecture de la quinzième ligne
    data = quinzieme_ligne.split()  # Séparation de la quinzième ligne en une liste de chaînes de caractères
    I0.append(data)  # Ajout de la quinzième colonne à la liste I0
somme_de_liste = I0 - I1
print(somme_de_liste)
