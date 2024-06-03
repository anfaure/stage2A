# Importation des bibliothèques 
import math
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

num_scan = 5

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    # Vérification pour éviter la division par zéro
    if I1 == I1bckg or I1 == 0:
        return 0
    else:
        return math.log10((I0 - I0bckg) / (I1 - I1bckg))

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne (longueurs d'onde)
    longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde] # Mettre la liste en float

# Fonction pour récupérer les données des scans
def recuperer_donnees_scan(f, num_scan, liste_I0bckg, liste_I1bckg):
    liste_I0 = []
    liste_I1 = []
    delay_scan = []
    try:
        for _ in range(8 + (num_scan - 1) * 3306):  # Ignorer les lignes avant le scan
            next(f)
        ligne_courante = next(f)
    
        while f"scan {num_scan}" in ligne_courante:
            element = ligne_courante.split()
            # Récupération du delay
            delay_scan.append(float(element[4]))
            for _ in range(2):
                next(f)

            ligne_courante = next(f)
            I1 = [float(x) for x in next(f).split()]
            ligne_courante = next(f)
            I0 = [float(x) for x in next(f).split()]

            next(f)  # saut de ligne
            ligne_courante = next(f)
            liste_I1.append(I1)
            liste_I0.append(I0)
    except StopIteration:
        pass
    return liste_I0, liste_I1, delay_scan

# Récupération des données pour chaque scan
liste_delta_OD = []
delay_scans = []
with open(file_path, 'r') as f:
    liste_I0bckg = []
    liste_I1bckg = []
    for i in range(num_scan):
        for _ in range(6 + ((num_scan - 1) * 3306)):  # Ignorer les lignes avant le scan
            next(f)
        I1bckg = [float(x) for x in next(f).split()]
        print(I1bckg[:2]) # Lecture de la ligne I1bckg et conversion en float
        I0bckg = [float(x) for x in next(f).split()]  # Lecture de la ligne I0bckg et conversion en float
        liste_I1bckg.append(I1bckg)
        liste_I0bckg.append(I0bckg)

        liste_I0, liste_I1, delay_scan = recuperer_donnees_scan(f, i, liste_I0bckg, liste_I1bckg)
        delay_scans.append(delay_scan)
        delta_OD_scan = []
        for j in range(len(liste_I0)):
            delta_OD = [calculer_delta_OD(liste_I0[j][k], liste_I0bckg[j][k], liste_I1[j][k], liste_I1bckg[j][k]) for k in range(len(liste_I0[j]))]
            delta_OD_scan.append(delta_OD)
        liste_delta_OD.append(delta_OD_scan)

# Création de la colormap
colors = ['#33b8ff', '#ff3333', '#68ff33']  # Couleurs de départ (bleu), de fin(rouge), et intermédiaires (vert)
cm = LinearSegmentedColormap.from_list('custom', colors, N=5)  # Utilisation de N=5

# Conversion des listes de délai en float
delay_scans = [[float(x) for x in delay_scan] for delay_scan in delay_scans]

# Création de la figure et des axes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Tracer le graphique 3D

for i in range(len(delay_scan)):
    X, Y = longueurs_donde, [delay_scan[i]] * len(longueurs_donde)
    Z = liste_delta_OD[i]
    ax.plot(X, Y, Z)

# Ajouter les étiquettes des axes
ax.set_xlabel('Longueur d\'onde (nm)')
ax.set_ylabel('Delay (ps)')
ax.set_zlabel('ΔOD')
plt.show()