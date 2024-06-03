# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np  # Importation de la bibliothèque NumPy


with open(file_path, 'r') as f:
    lines = f.readlines()

with open(file_path, 'r') as f:
    I1bckg = []  # Création d'une liste vide pour stocker les I1bckg
    for _ in range(6):  # Ignorer les 6 premières lignes
        next(f)
    septieme_ligne = next(f)  # Lecture de la septième ligne
    data = septieme_ligne.split()  # Séparation de la septième ligne en une liste de chaînes de caractères
    I1bckg.append(data)  # Ajout de la septième colonne à la liste I1bckg
    I0bckg = []
    for _ in range(8):  # Ignorer les 8 premières lignes
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la neuvième ligne
    data = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I0bckg.append(data)  # Ajout de la neuvième colonne à la liste I0bckg


# Lecture des données
with open(file_path, 'r') as f:
    I1 = []  # Création d'une liste vide pour stocker les I1
    for _ in range(7):  # Ignorer les 12 premières lignes
        next(f)
    for _ in range (2):
        for _ in range(5):  # Ignorer les 12 premières lignes
            next(f)
        I1 = next(f)  # Lecture de la quatrième ligne
        data = I1.split()  # Séparation de la quatrième ligne en une liste de chaînes de caractères
        I1.append(data)  # Ajout de la quatrième colonne à la liste I1
        

    
    I0 = []
    for _ in range(14):  # Ignorer les 14 premières lignes
        next(f)
    quinzieme_ligne = next(f)  # Lecture de la quinzième ligne
    data = quinzieme_ligne.split()  # Séparation de la quinzième ligne en une liste de chaînes de caractères
    I0.append(data)  # Ajout de la quinzième colonne à la liste I0
print(I1)