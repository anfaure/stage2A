# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x =( (I0 - I0bckg) / (I1 - I1bckg))
    delta_OD = 0 if x <= 0 else math.log10(x)
    return delta_OD

# Lecture des longueurs d'onde
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne (longueurs d'onde)
    longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde] # Conversion en float

# Fonction pour lire les scans et récupérer les données
def lire_scan(file_path, start_line, scan_label):
    with open(file_path, 'r') as f:
        for _ in range(start_line):
            next(f)
        septieme_ligne = next(f)
        I1bckg = [float(x) for x in septieme_ligne.split()]
        for _ in range(2):
            next(f)
        neuvieme_ligne = next(f)
        I0bckg = [float(x) for x in neuvieme_ligne.split()]
        
    with open(file_path, 'r') as f:
        liste_I0 = []
        liste_I1 = []
        delay = []
        for _ in range(start_line + 4):
            next(f)
        ligne_courante = next(f)
        while scan_label in ligne_courante:
            element = ligne_courante.split()
            delay.append(float(element[4]))
            for _ in range(2):
                next(f)
            ligne_courante = next(f)
            liste_I1.append([float(x) for x in ligne_courante.split()])
            ligne_courante = next(f)
            liste_I0.append([float(x) for x in ligne_courante.split()])
            next(f)
            ligne_courante = next(f)
    return liste_I0, liste_I1, I0bckg, I1bckg, delay

# Lecture des scans
scan_data = [
    lire_scan(file_path, 6, "scan 1"),
    lire_scan(file_path, 3312, "scan 2"),
    lire_scan(file_path, 6618, "scan 3"),
    lire_scan(file_path, 9924, "scan 4"),
    #lire_scan(file_path, 13230, "scan 5")
]


# Calcul des ΔOD pour chaque scan
liste_delta_od = []
for I0, I1, I0bckg, I1bckg, delay in scan_data:
    delta_ODs = []
    for i in range(len(I0)):
        delta_od = []
        for j in range(len(I0[i])):
            delta_od.append(calculer_delta_OD(I1[i][j], I1bckg[j], I0[i][j], I0bckg[j]))
        delta_ODs.append(delta_od)
    liste_delta_od.append(delta_ODs)


from matplotlib.colors import LinearSegmentedColormap

# Création du plot
fig, ax = plt.subplots()
ax.set_xlim([450, 900])
ax.set_ylim([-4,10])
for scan_index, (delta_od, delay) in enumerate(zip(liste_delta_od, [data[4] for data in scan_data])):
    for i in range(len(delay)):
        c = ax.pcolormesh(longueurs_donde, delay, delta_od[i], vmin=-0.001, vmax=0.001)
        
# Plot des données avec une colormap

# Définir l'échelle de Delta OD
vmin = -0.005  # Valeur minimale de Delta OD
vmax = 1  # Valeur maximale de Delta OD
# Ajouter une barre de couleur
cbar = fig.colorbar(c, ax=ax)
cbar.set_label('Delta OD')

# Ajouter les labels et le titre
ax.set_xlabel('Longueur d\'onde (nm)')
ax.set_ylabel('Délai (ps)')# Afficher le plot
plt.show()