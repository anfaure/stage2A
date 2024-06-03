# Ouverture du fichier en mode lecture
import math
import matplotlib.pyplot as plt
import numpy as np  # Importation de la bibliothèque NumPy

file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
   x = (I1 - I1bckg)
   delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
   return delta_OD


# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    for _ in range(3):  # Ignorer les 3 premières lignes
        next(f)
    quatrieme_ligne = next(f)  # Lecture de la quatrième ligne
    longueurs_donde = quatrieme_ligne.split() [1:]  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]

    
# scan5
# Récupération I1 et I0 bckg
    for _ in range(13226):
        next(f)
    septieme_ligne = next(f)  # Lecture de la ligne I1bckg
    I1bckg_scan5 = septieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
    I1bckg_scan5 = [float(x) for x in I1bckg_scan5]

    for _ in range(2):  
        next(f)
    neuvieme_ligne = next(f)  # Lecture de la ligne I0bckg
    I0bckg_scan5 = neuvieme_ligne.split()  # Séparation de la ligne en une liste de chaînes de caractères
    I0bckg_scan5 = [float(x) for x in I0bckg_scan5]

    ligne_courante = next(f)

with open(file_path, 'r') as f:
    liste_I0_scan5 = []
    delay_scan_5 = []# Création d'une liste vide pour stocker les données
    for _ in range(13234):
        next(f)
   
    for _ in range(550):
        for _ in range(4):
            next(f)

        ligne_courante = next(f)
        liste_I0_scan5.append([float(x) for x in ligne_courante.split()])
        
        for _ in range(1):
            next(f) # saut de ligne

with open(file_path, 'r') as f:
    liste_I1_scan5 = []  
    delay_scan_5 = []# Création d'une liste vide pour stocker les données
    for _ in range(13234):
        next(f)
   
    for _ in range(550):
        for _ in range(2):
            next(f)

        ligne_courante = next(f)
        liste_I1_scan5.append([float(x) for x in ligne_courante.split()])

        for _ in range(3):
            next(f) # saut de ligne

with open(file_path, 'r') as f:
        delay_scan_5 = []# Création d'une liste vide pour stocker les données
        for _ in range(1):
            next(f)
           
        for _ in range(550):
            element = ligne_courante.split() 
        # Récupération du delay
            delay_scan_5.append(float(element[4]))
            for _ in range(5):
                next(f)  
                                
# Création liste
liste_delta_OD_5 = []
for i in range(len(liste_I0_scan5)):
    # Calcul de delta_OD pour scan5
    delta_OD = []
    for j in range(len(liste_I0_scan5[i])):
        delta_OD.append(calculer_delta_OD(liste_I0_scan5[i][j], I0bckg_scan5[j],
                                                liste_I1_scan5[i][j], I1bckg_scan5[j]))
    liste_delta_OD_5.append(delta_OD)

# Generate example data
x = longueurs_donde  # Wavelength (nm)
y = delay_scan_5     # Delay (ps)
X, Y = np.meshgrid(x, y)
Z = delay_scan_5

# Create the plot
plt.figure(figsize=(6, 5))
plt.contourf(X, Y, Z, levels=100, cmap='jet')
plt.colorbar(label='Intensity')
plt.xlabel('Wavelength, nm')
plt.ylabel('Delay, ps')
plt.title('Reference used')
plt.show()