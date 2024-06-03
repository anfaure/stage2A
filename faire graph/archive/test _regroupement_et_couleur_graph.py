# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

import math
import matplotlib.pyplot as plt
import numpy as np  # Importation des bibliothèques 

num_scan = 5

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I0 - I0bckg) / (I1 - I1bckg)
    delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne (longueurs d'onde)
    longueurs_donde = quatrieme_ligne.split() [1:]  # Séparation de la ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde] # Mettre la liste en float

# Scan 1
    # Récupération I1 et I0 bckg scan1
with open(file_path, 'r') as f:
    for _ in range(6):  
        next(f)
    septieme_ligne = next(f)  # Lecture de la ligne I1bckg
    I1bckg_scan1 = septieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
    I1bckg_scan1 = [float(x) for x in I1bckg_scan1] # Mettre les valeurs en float

    for _ in range(2):
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la ligne I0bckg
    I0bckg_scan1 = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I0bckg_scan1 = [float(x) for x in I0bckg_scan1]

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    liste_I0_scan1 = []
    liste_I1_scan1 = []
    delay_scan_1 = []
    for _ in range(10):
        next(f)
    ligne_courante  = next(f)
    while "scan 1" in ligne_courante: #tant qu'il y a scan 1 sur la ligne il exécute la boucle  
        element = ligne_courante.split()
        # Récupération du delay
        delay_scan_1.append(float(element[4]))
        for _ in range(2):
            next(f)

        ligne_courante = next(f)
        liste_I1_scan1.append([float(x) for x in ligne_courante.split()])

        ligne_courante = next(f)
        liste_I0_scan1.append([float(x) for x in ligne_courante.split()])
        
        next(f)
        ligne_courante = next(f)

# Création liste
liste_delta_OD_1 = []
for i in range(len(liste_I0_scan1)):
    # Calcul de delta_OD pour scan 1
    delta_OD = []
    for j in range(len(liste_I0_scan1[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan1[i][j], I0bckg_scan1[j],
                                                liste_I1_scan1[i][j], I1bckg_scan1[j])) # prendre la valeur i(ligne) de j(colonne)
    liste_delta_OD_1.append(delta_OD)


# Scan 2
with open(file_path, 'r') as f:
# Récupération I1 et I0 bckg scan2
    for _ in range(3312):
        next(f)
    septieme_ligne = next(f)  # Lecture de la ligne I1bckg_scan2
    I1bckg_scan2 = septieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
    I1bckg_scan2 = [float(x) for x in I1bckg_scan2]

    for _ in range(2):
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la ligne I0bckg_scan2
    I0bckg_scan2 = neuvieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
    I0bckg_scan2 = [float(x) for x in I0bckg_scan2]

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    liste_I0_scan2= []
    liste_I1_scan2 = []
    delay_scan_2 = []  # Création d'une liste vide pour stocker les données
    for _ in range(3316):
        next(f)
    ligne_courante  = next(f)
    while "scan 2" in ligne_courante:
        element = ligne_courante.split()
        # Récupération du delay
        delay_scan_2.append(float(element[4]))
        for _ in range(2):
            next(f)

        ligne_courante = next(f)
        liste_I1_scan2.append([float(x) for x in ligne_courante.split()])

        ligne_courante = next(f)
        liste_I0_scan2.append([float(x) for x in ligne_courante.split()])
        
        next(f) # saut de ligne
        ligne_courante = next(f)

# Création liste
liste_delta_OD_2 = []
for i in range(len(liste_I0_scan2)):
    # Calcul de delta_OD pour série d'enregistrement
    delta_OD = []
    for j in range(len(liste_I0_scan2[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan2[i][j], I0bckg_scan2[j],
                                                liste_I1_scan2[i][j], I1bckg_scan2[j]))
    liste_delta_OD_2.append(delta_OD)

# Scan 3
# Récupération I1 et I0 bckg
with open(file_path, 'r') as f:
    for _ in range(6618):  # Ignorer les 5 premières lignes
        next(f)
    septieme_ligne = next(f)  # Lecture de la septième ligne
    I1bckg_scan3 = septieme_ligne.split()  # Séparation de la septième ligne en une liste de chaînes de caractères
    I1bckg_scan3 = [float(x) for x in I1bckg_scan3]

    for _ in range(2):  # Ignorer les 7 premières lignes
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la neuvième ligne
    I0bckg_scan3 = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I0bckg_scan3 = [float(x) for x in I0bckg_scan3]

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    liste_I0_scan3 = []
    liste_I1_scan3 = [] 
    delay_scan_3 = [] # Création d'une liste vide pour stocker les données
    for _ in range(6622):  # Ignorer les 12 premières lignes
        next(f)
    ligne_courante  = next(f)
    while "scan 3" in ligne_courante:
        element = ligne_courante.split()
        # Récupération du delay
        delay_scan_3.append(float(element[4]))
        for _ in range(2):
            next(f)

        ligne_courante = next(f)
        liste_I1_scan3.append([float(x) for x in ligne_courante.split()])

        ligne_courante = next(f)
        liste_I0_scan3.append([float(x) for x in ligne_courante.split()])
        
        next(f) # saut de ligne
        ligne_courante = next(f)

# Création liste
liste_delta_OD_3 = []
for i in range(len(liste_I0_scan3)):
    # Calcul de delta_OD pour série d'enregistrement
    delta_OD = []
    for j in range(len(liste_I0_scan3[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan3[i][j], I0bckg_scan3[j],
                                                liste_I1_scan3[i][j], I1bckg_scan3[j]))
    liste_delta_OD_3.append(delta_OD)

#scan4 
with open(file_path,'r') as f:
# Récupération I1 et I0 bckg
    for _ in range(9924):  # Ignorer les 5 premières lignes
        next(f)
    septieme_ligne = next(f)  # Lecture de la septième ligne
    I1bckg_scan4 = septieme_ligne.split()  # Séparation de la septième ligne en une liste de chaînes de caractères
    I1bckg_scan4 = [float(x) for x in I1bckg_scan4]

    for _ in range(2):  # Ignorer les 7 premières lignes
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la neuvième ligne
    I0bckg_scan4 = neuvieme_ligne.split()  # Séparation de la neuvième ligne en une liste de chaînes de caractères
    I0bckg_scan4 = [float(x) for x in I0bckg_scan4]

with open(file_path, 'r') as f:
    liste_I0_scan4 = []
    liste_I1_scan4 = []  
    delay_scan_4 = []# Création d'une liste vide pour stocker les données
    for _ in range(9928):  # Ignorer les 12 premières lignes
        next(f)
    ligne_courante  = next(f)
    
    while "scan 4" in ligne_courante:
        element = ligne_courante.split()
        # Récupération du delay
        delay_scan_4.append(float(element[4]))
        for _ in range(2):
            next(f)
        ligne_courante = next(f)
        liste_I1_scan4.append([float(x) for x in ligne_courante.split()])
        ligne_courante = next(f)
        liste_I0_scan4.append([float(x) for x in ligne_courante.split()])
        next(f) # saut de ligne
        ligne_courante = next(f)

# Création liste
liste_delta_OD_4 = []
for i in range(len(liste_I0_scan4)):
    # Calcul de delta_OD pour scan4 
    delta_OD = []
    for j in range(len(liste_I0_scan4[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan4[i][j], I0bckg_scan4[j],
                                                liste_I1_scan4[i][j], I1bckg_scan4[j]))
    liste_delta_OD_4.append(delta_OD)

#scan5
# Récupération I1 et I0 bckg
#with open(file_path, 'r') as f:
#    for _ in range(13230):
#        next(f)
#    septieme_ligne = next(f)  # Lecture de la ligne I1bckg
#    I1bckg_scan5 = septieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
#    I1bckg_scan5 = [float(x) for x in I1bckg_scan5]

#    for _ in range(2):  
#        next(f)
#    neuvieme_ligne = next(f)  # Lecture de la ligne I0bckg
#    I0bckg_scan5 = neuvieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
#    I0bckg_scan5 = [float(x) for x in I0bckg_scan5]


#with open(file_path, 'r') as f:
#    liste_I0_scan5 = []
#    liste_I1_scan5 = []  
#    delay_scan_5 = []# Création d'une liste vide pour stocker les données
#    for _ in range(13234):
#        next(f)
    
#    try:
#        while True:
#            element = ligne_courante.split()
        # Récupération du delay
#            delay_scan_5.append(float(element[4]))
#            for _ in range(2):
#                next(f)
#            ligne_courante = next(f)
#            liste_I1_scan5.append([float(x) for x in ligne_courante.split()])
#            ligne_courante = next(f)
#            liste_I0_scan5.append([float(x) for x in ligne_courante.split()])
#            for _ in range(2):
#                next(f) 
#    except StopIteration:
#        pass

# Création liste
#liste_delta_OD_5 = []
#for i in range(len(liste_I0_scan5)):
#    # Calcul de delta_OD pour scan5
#    delta_OD = []
#    for j in range(len(liste_I0_scan5[i])):
#        delta_OD.append(calculer_delta_OD(liste_I0_scan5[i][j], I0bckg_scan5[j],
#                                                liste_I1_scan5[i][j], I1bckg_scan5[j]))
#    liste_delta_OD_5.append(delta_OD)


from matplotlib.colors import LinearSegmentedColormap

# Création d'une colormap dégradée
colors = ['#33b8ff', '#ff3333', '#68ff33']  # Couleurs de départ (bleu), de fin(rouge), et intermédiaires (vert)
cm = LinearSegmentedColormap.from_list('custom', colors, N=len(liste_I0_scan1))

delay_scan_1 = [float(x) for x in delay_scan_1]
delay_scan_2 = [float(x) for x in delay_scan_2]
delay_scan_3 = [float(x) for x in delay_scan_3]
delay_scan_4 = [float(x) for x in delay_scan_4]
#delay_scan_5 = [float(x) for x in delay_scan_5]
delay_scans = [delay_scan_1, delay_scan_2, delay_scan_3, delay_scan_4]#, delay_scan_5]

liste_delta_OD = np.array([liste_delta_OD_1, liste_delta_OD_2, liste_delta_OD_3, liste_delta_OD_4])#, liste_delta_OD_5])
#print(len(delay_scan_5), len(liste_delta_OD_5))
from mpl_toolkits.mplot3d import Axes3D

# Création de la figure et des axes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Tracer le graphique 3D

X, Y = np.meshgrid(np.arange(len(longueurs_donde)), np.arange(len(delay_scans)))
X = X.flatten()
Y = Y.flatten()
Z = np.zeros_like(X)

for i, (x,y) in enumerate(zip (X,Y)):
    Z[i] = liste_delta_OD[y][x]

ax.scatter(X,Y,Z)

#for i in range(len(delay_scans)):
#    X, Y = longueurs_donde, [delay_scans[i]] * len(longueurs_donde)
#    Z = liste_delta_OD[i]
#    ax.plot(X, Y, Z)

# Ajouter les étiquettes des axes
ax.set_xlabel('Longueur d\'onde (nm)')
ax.set_ylabel('Delay (ps)')
ax.set_zlabel('ΔOD')
plt.show()












# Tracer le graphe
for i in range(len(liste_I0_scan2)):
    plt.plot(longueurs_donde, liste_delta_OD_2[i], linestyle='-', color='#68ff33') # Tracer le graphe
    plt.plot(longueurs_donde, liste_delta_OD_1[i], linestyle='-', color='#ff9f33')
    plt.plot(longueurs_donde, liste_delta_OD_3[i], linestyle='-', color='#33c1ff')
    plt.plot(longueurs_donde, liste_delta_OD_4[i], linestyle='-', color='#9c33ff')
    #plt.plot(longueurs_donde, liste_delta_OD_5[i], linestyle='-', color='#ff33bb')
plt.xlabel('Longueur d\'onde (nm)') # Titre abscisse
plt.ylabel('ΔOD') # Titre ordonnée
plt.title("ΔOD en fonction de la longueur d'onde") # Titre du graphe
plt.grid(True) # Afficher la grille
plt.show() # Afficher le graphe