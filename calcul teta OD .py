import math
import matplotlib.pyplot as plt


#lire le fichier .dat
import numpy as np  # Importation de la bibliothèque NumPy
import pandas as pd  # Importation de la bibliothèque Pandas

# Fonction pour calculer ΔOD
def calculer_ΔOD(I0, I0bckg, I1, I1bckg):
    ΔOD = math.log10((I0 - I0bckg) / (I1 / I1bckg))
    return ΔOD

# Ouverture du fichier en mode lecture
with open('/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat', 'r') as f:
    longueurs_donde = []  # Création d'une liste vide pour stocker les longueurs d'onde
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne
    data = quatrieme_ligne.split()  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde.append(data[3])  # Ajout de la quatrième colonne à la liste longueurs_donde


# Ouverture du fichier en mode lecture
with open('/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat', 'r') as f:
    val = []  # Création d'une liste vide pour stocker les données
    for _ in range(6):  # Ignorer les 6 premières lignes
        next(3305)
    for line in 3305:  # Parcours de chaque ligne du fichier
        data = line.split()  # Séparation de chaque ligne en une liste de chaînes de caractères
        Pump = data[0]  # Première colonne
        I0.append(data[1])  # Deuxième colonne
        I0bckg.append(data[2])  # Troisième colonne
        I1.append(data[3])  # Quatrième colonne
        I1bckg.append(data[4])  # Cinquième colonne
        Measurement.append(data[5])  # Sixième colonne

# Création d'un DataFrame Pandas à partir de la liste de données
matrix_data = pd.DataFrame(data)

# Données de I
I0 = data[1]
I0bckg = data [2]
I1 = data [3]
I1bckg = data [4]

# Calcul des ΔOD
ΔOD = [calculer_ΔOD(IO, I0bckg, I1, I1bckg) for I0, I0bckg, I1, I1bckg in zip(longueurs_donde, ΔOD, longueurs_donde, ΔOD)]

# Tracer le graphe
plt.plot(longueurs_donde, ΔOD, marker='o', linestyle='-')
plt.xlabel('Longueur d\'onde')
plt.ylabel('ΔOD')
plt.title('Graphe de ΔOD en fonction de la longueur d\'onde')
plt.grid(True)
plt.show()