# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt

# Lire le fichier .dat
import numpy as np  # Importation de la bibliothèque NumPy

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    longueurs_donde = []  # Création d'une liste vide pour stocker les longueurs d'onde
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne
    data = quatrieme_ligne.split() [1:]  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde.append(data)  # Ajout de la quatrième colonne à la liste longueurs_donde


print(longueurs_donde)