import os
import math
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = I1 - I1bckg
    delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD

# Demander à l'utilisateur le chemin du fichier à examiner
file_path = input("Entrez le chemin du fichier à examiner : ")
#'/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'
# Vérifier si le fichier existe
if not os.path.isfile(file_path):
    print("Le fichier n'existe pas. Veuillez entrer un chemin valide.")
    exit()
print(f"Le chemin du fichier à examiner est : {file_path}")

# Lire les longueurs d'onde
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne (longueurs d'onde)
    longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]  # Conversion en float

# Lire les délais
delay = []
with open(file_path, 'r') as f:
    for _ in range(10):
        next(f)
    ligne_courante = next(f)
    while "scan 1" in ligne_courante:  # tant qu'il y a scan 1 sur la ligne il exécute la boucle
        element = ligne_courante.split()
        # Récupération du delay
        delay.append(float(element[4]))
        for _ in range(5):
            next(f)
        ligne_courante = next(f)
print(len(delay))

# Récupérer le nombre de scans
with open(file_path, 'r') as file:
    lines = file.readlines()
scan_numbers = [int(re.search(r"scan (\d+)", line).group(1)) for line in lines if re.search(r"scan (\d+)", line)]
scan_number = max(scan_numbers)
print(f"Nombre de scans trouvés : {scan_number}")

# Initialiser les listes pour les valeurs
liste_I0bckg = [[] for _ in range(scan_number)]
liste_I1bckg = [[] for _ in range(scan_number)]
liste_I0 = [[] for _ in range(scan_number)]
liste_I1 = [[] for _ in range(scan_number)]

# Lire les données des fichiers et remplir les listes
for i in range(scan_number):
    # Récupération I1 et I0 bckg
    with open(file_path, 'r') as f:
        for _ in range(4 + (i * 3306)):  # Ignorer les lignes avant le scan
            next(f)
        for _ in range(3): 
            next(f)
        I1bckg = [float(x) for x in next(f).split()]  # Lecture de la ligne I1bckg et conversion en float
        I0bckg = [float(x) for x in next(f).split()]  # Lecture de la ligne I0bckg et conversion en float
        liste_I1bckg[i] = I1bckg
        liste_I0bckg[i] = I0bckg

# Lire les données de I0 et I1
with open(file_path, 'r') as f:
    for _ in range(10):
        next(f)
        
    for i in range(scan_number):
        I0_scan = []
        I1_scan = []
        for j in range(len(delay)):
            for _ in range(3):  # Sauter 3 lignes
                next(f)

            # Lire les données de I1
            ligne_courante = next(f)
            I1 = [float(x) for x in ligne_courante.split()]

            # Lire les données de I0
            ligne_courante = next(f)
            I0 = [float(x) for x in ligne_courante.split()]
            next(f)
            I0_scan.append(I0)
            I1_scan.append(I1)
        liste_I0[i] = I0_scan
        liste_I1[i] = I1_scan

# Calculer delta_OD
liste_delta_OD = [[] for _ in range(scan_number)]
for i in range(scan_number):
    delta_OD = []
    for j in range(len(liste_I0[i])):
        for k in range(len(liste_I0[i][j])):
            delta_OD.append(calculer_delta_OD(liste_I0[i][j][k], liste_I0bckg[i][k],
                                              liste_I1[i][j][k], liste_I1bckg[i][k]))
    liste_delta_OD[i] = delta_OD
from matplotlib.colors import LinearSegmentedColormap

# Demander à l'utilisateur la longueur d'onde à examiner
nombre_scan =  int(input("Entrez le nombre de scan à examiner (1-5) : "))

# Demander à l'utilisateur les numéros des scans à examiner
scans_a_examiner = []
for i in range(nombre_scan):
    scan_num = int(input(f"Entrez le numéro du scan {i+1} à examiner (1-5) : ")) - 1
    scans_a_examiner.append(scan_num)

# Définir les couleurs pour la colormap
colors = ['#edfa2f', '#0db21b', '#ffffff', '#1b39cf', '#da2ffa'] 
cm = LinearSegmentedColormap.from_list('custom', colors, N=256)
ax=[]
# Création de la figure avec plusieurs sous-graphes
fig, axs = plt.subplots(ncols=nombre_scan, figsize=(14, 6))

# Afficher les scans choisis
for i in range(nombre_scan):
    scan_num = scans_a_examiner[i]
    axs[i].set_xlim([450, 900])
    axs[i].set_ylim([-4,10])
    c = axs[i].pcolormesh(longueurs_donde, delay, liste_delta_OD[scan_num], cmap=cm, vmin=-0.001, vmax=0.001)
    cbar1 = fig.colorbar(c, ax=axs[i])
    cbar1.set_label('Delta OD')
    axs[i].set_xlabel('Longueur d\'onde (nm)')
    axs[i].set_ylabel('Délai (ps)')
    axs[i].set_title(f'Scan {scan_num + 1} ')

# Afficher le graphique
plt.tight_layout()
plt.show()
for i, scan_num in enumerate(range(scan_number)):
    c = axs[i].pcolormesh(longueurs_donde, delay, liste_delta_OD[scan_num], cmap=cm, vmin=-0.001, vmax=0.001)
    axs[i].set_title(f'Scan {scan_num + 1}')
    axs[i].set_xlabel('Longueur d\'onde')
    axs[i].set_ylabel('Delay')

fig.colorbar(c, ax=axs, orientation='vertical')
plt.show()
