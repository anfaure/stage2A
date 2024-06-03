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


# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne
    longueurs_donde = quatrieme_ligne.split() [1:]  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]

    
    # Récupération I1 et I0 bckg
    for _ in range(13226):  # Ignorer les 5 premières lignes
        next(f)
    septieme_ligne = next(f)  # Lecture de la septième ligne
    I0bckg_scan5 = septieme_ligne.split()  # Séparation de la septième ligne en une liste de chaînes de caractères
    I0bckg_scan5 = [float(x) for x in I0bckg_scan5]

    for _ in range(2):  # Ignorer les 7 premières lignes
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la neuvième ligne
    I1bckg_scan5 = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I1bckg_scan5 = [float(x) for x in I1bckg_scan5]

# Scan 5
# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    liste_I0_scan5 = []
    liste_I1_scan5 = []  # Création d'une liste vide pour stocker les données
    ligne_courante  = next(f)
    for _ in range(13234):  # Ignrer les 12 premières lignes
        next(f) 
    try:
        while True:
            for _ in range(2):
                next(f)

            ligne_courante = next(f)
            liste_I0_scan5.append([float(x) for x in ligne_courante.split()])

            ligne_courante = next(f)
            liste_I1_scan5.append([float(x) for x in ligne_courante.split()])
            
            next(f) # saut de ligne

    except StopIteration:
        pass
        
# Création liste
liste_delta_OD_5 = []
for i in range(len(liste_I0_scan5)):
    # Calcul de delta_OD pour série d'enregistrement
    delta_OD = []
    for j in range(len(liste_I0_scan5[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan5[i][j], I0bckg_scan5[j],
                                                liste_I1_scan5[i][j], I1bckg_scan5[j]))
    liste_delta_OD_5.append(delta_OD)

# Tracer le graphe
for i in range(len(liste_I0_scan5)):
    plt.plot(longueurs_donde, liste_delta_OD_5[i], linestyle='-') # Tracer le graphe
plt.xlabel('Longueur d\'onde (nm)') # Titre abscisse
plt.ylabel('ΔOD') # Titre ordonnée
plt.title("Graphe de ΔOD en fonction de la longueur d'onde") # Titre du graphe
plt.grid(True) # Afficher la grille
plt.show() # Afficher le graphe