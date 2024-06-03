import os
import math
import matplotlib.pyplot as plt
import re

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I0 - I0bckg) / (I1 - I1bckg)
    delta_OD = 0 if x <= 0 else math.log10(x)
    return delta_OD

# Demander à l'utilisateur le chemin du fichier à examiner
file_path = input("Entrez le chemin du fichier à examiner : ")
# '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'
# Vérifier si le fichier existe
if not os.path.isfile(file_path):
    print("Le fichier n'existe pas. Veuillez entrer un chemin valide.")
    exit()

print(f"Le chemin du fichier à examiner est : {file_path}")

# Récupérer le nombre de scans
with open(file_path, 'r') as file:
    lines = file.readlines()
scan_numbers = [int(re.search(r"scan (\d+)", line).group(1)) for line in lines if re.search(r"scan (\d+)", line)]
scan_number = max(scan_numbers)
print(f"Nombre de scans trouvés : {scan_number}")

# Lire les longueurs d'onde
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne (longueurs d'onde)
    longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]  # Conversion en float

def lire_bckg(f, scan_number):
    """Lire les lignes de fond I1bckg et I0bckg à partir du décalage donné"""
    for _ in range(4 + ((scan_number-1) * 3306)):
        next(f)
    I1bckg = next(f).split()
    I1bckg = [float(x) for x in I1bckg]
    for _ in range(2):
        next(f)
    I0bckg = next(f).split()
    I0bckg = [float(x) for x in I0bckg]
    return I1bckg, I0bckg

def lire_scan(f, scan_number):
    """Lire les données de I0 et I1 pour un scan donné à partir du décalage donné"""
    liste_I0 = []
    liste_I1 = []
    delay = []

    for _ in range(10+scan_number):
        next(f)
    ligne_courante = next(f)

    while f"scan {scan_number}" in ligne_courante:
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

    return liste_I0, liste_I1, delay

def traitement_scan(file_path, scan_numbers):
    """Traiter les scans spécifiés et calculer delta_OD"""
    liste_delta_OD = []
    delays = []

    with open(file_path, 'r') as f:
        for scan_number in scan_numbers:
            I1bckg, I0bckg = lire_bckg(f, 0)
            f.seek(0)  # Réinitialiser le fichier pour la lecture du scan
            liste_I0, liste_I1, delay = lire_scan(f, 4, scan_number)

            delta_OD_scan = []
            for i in range(len(liste_I0)):
                delta_OD = []
                for j in range(len(liste_I0[i])):
                    delta_OD.append(calculer_delta_OD(liste_I0[i][j], I0bckg[j], liste_I1[i][j], I1bckg[j]))
                delta_OD_scan.append(delta_OD)
            liste_delta_OD.append(delta_OD_scan)
            delays.append(delay)
    return liste_delta_OD, delays

# Demander à l'utilisateur la longueur d'onde à examiner
longueur_donde_a_examiner = float(input("Entrez la longueur d'onde à examiner (nm) : "))

# Demander à l'utilisateur le nombre de scans à examiner
nombre_scan = int(input("Entrez le nombre de scans à examiner : "))

# Demander à l'utilisateur les numéros des scans à examiner
scans_a_examiner = []
for i in range(nombre_scan):
    scan_num = int(input(f"Entrez le numéro du scan {i + 1} à examiner : "))
    scans_a_examiner.append(scan_num)

# Traiter les scans spécifiés
liste_delta_OD, delays = traitement_scan(file_path, scans_a_examiner)

# Trouver l'indice de la longueur d'onde correspondante
try:
    indice_longueur_donde = longueurs_donde.index(longueur_donde_a_examiner)
except ValueError:
    valeur_plus_proche = min(longueurs_donde, key=lambda x: abs(x - longueur_donde_a_examiner))
    indice_longueur_donde = longueurs_donde.index(valeur_plus_proche)

# Extraire les valeurs de ΔOD pour la longueur d'onde spécifiée pour chaque scan
delta_OD_a_examiner = []
for scan_index in range(len(scans_a_examiner)):
    scan = liste_delta_OD[scan_index]
    delta_OD_a_examiner.append([row[indice_longueur_donde] for row in scan])

# Tracer le graphe
for i, delta_OD in enumerate(delta_OD_a_examiner):
    plt.plot(delays[i], delta_OD, label=f'Scan {scans_a_examiner[i]}')

plt.xlabel('Delay (ns)')  # Titre abscisse
plt.ylabel('ΔOD')  # Titre ordonnée
plt.title(f"Graphe de ΔOD en fonction du delay pour la longueur d'onde {longueur_donde_a_examiner} nm")  # Titre du graphe
plt.legend()
plt.grid(True)  # Afficher la grille
plt.show()  # Afficher le graphe
