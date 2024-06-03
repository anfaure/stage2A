# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np  # Importation de la bibliothèque NumPy

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I0 - I0bckg) / (I1 - I1bckg)
    delta_OD = math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD


# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne
    longueurs_donde = quatrieme_ligne.split() [1:]  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]

    
    # Récupération I1 et I0 bckg
    for _ in range(2):  # Ignorer les 5 premières lignes
        next(f)
    septieme_ligne = next(f)  # Lecture de la septième ligne
    I0bckg = septieme_ligne.split()  # Séparation de la septième ligne en une liste de chaînes de caractères
    I0bckg = [float(x) for x in I0bckg]

    for _ in range(2):  # Ignorer les 7 premières lignes
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la neuvième ligne
    I1bckg = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I1bckg = [float(x) for x in I1bckg]

# Scan 1
# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    liste_I0_scan1 = []
    liste_I1_scan1 = []
    for _ in range(10):  # Ignorer les 12 premières lignes
        next(f)
    ligne_courante  = next(f)
    while "scan 1" in ligne_courante:
        for _ in range(2):
            next(f)

        ligne_courante = next(f)
        liste_I1_scan1.append([float(x) for x in ligne_courante.split()])

        ligne_courante = next(f)
        liste_I0_scan1.append([float(x) for x in ligne_courante.split()])
        
        next(f) # saut de ligne
        ligne_courante = next(f)

# Création liste
liste_delta_OD = []
for i in range(len(liste_I0_scan1)):
    # Calcul de delta_OD pour série d'enregistrement
    delta_OD = []
    for j in range(len(liste_I0_scan1[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan1[i][j], I0bckg[j],
                                                liste_I1_scan1[i][j], I1bckg[j]))
    liste_delta_OD.append(delta_OD)

# Importation des bibliothèques supplémentaires
from matplotlib.colors import LinearSegmentedColormap

# Création d'une colormap dégradée
colors = ['#ff0000', '#00ff00', '#0000ff']  # Couleurs de départ, de fin, et intermédiaires
cm = LinearSegmentedColormap.from_list('custom', colors, N=len(liste_I0_scan1))

# Tracer le graphe avec coloration dégradée
for i in range(len(liste_I0_scan1)):
    plt.plot(longueurs_donde, liste_delta_OD[i], linestyle='-', color=cm(i)) # Utilisation de la couleur définie par la colormap
plt.xlabel('Longueur d\'onde (nm)') # Titre abscisse
plt.ylabel('ΔOD') # Titre ordonnée
plt.title("Graphe de ΔOD en fonction de la longueur d'onde") # Titre du graphe
plt.grid(True) # Afficher la grille
plt.show() # Afficher le graphe
