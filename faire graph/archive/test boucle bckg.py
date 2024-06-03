import math
import matplotlib.pyplot as plt

# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I0 - I0bckg) / (I1 - I1bckg)
    delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD

# Initialisation des listes pour stocker les valeurs lues à partir du fichier
longueurs_donde = []
I0bckg = []
I1bckg = []

# Ouverture du fichier en mode lecture
with open(file_path, 'r') as f:
    # Ignorer les 3 premières lignes
    for _ in range(3):
        next(f)

    # Lecture de la quatrième ligne pour récupérer les longueurs d'onde
    quatrieme_ligne = next(f)
    longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la quatrième ligne en une liste de chaînes de caractères
    longueurs_donde = [float(x) for x in longueurs_donde]

    # Ignorer les lignes jusqu'à la première occurrence de I0 et I1 bckg
    for _ in range(5):
        next(f)

    # Lecture des valeurs de I0bckg et I1bckg
    for _ in range(2):
        septieme_ligne = next(f)
        I0bckg_temp = septieme_ligne.split()[1:]
        I0bckg_temp = [float(x) for x in I0bckg_temp]
        I0bckg.append(I0bckg_temp)

        next(f)  # Ignorer la ligne suivante

        neuvieme_ligne = next(f)
        I1bckg_temp = neuvieme_ligne.split()[1:]
        I1bckg_temp = [float(x) for x in I1bckg_temp]
        I1bckg.append(I1bckg_temp)

# Vérifier la longueur de I0bckg
print(I0bckg)