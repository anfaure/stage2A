# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

# Liste pour stocker le nombre d'éléments sur chaque ligne
nombre_elements_par_ligne = []

# Ouvrir le fichier en mode lecture
with open(file_path, 'r') as file:
    # Parcourir chaque ligne du fichier
   # Ignorer les 6 premières lignes
    for _ in range(3):
        next(file)
    # Lire la septième ligne
    line_4 = file.readline()

# Séparer la ligne en éléments en utilisant l'espace comme séparateur
elements = line_4.split()
# Nombre d'éléments sur la ligne 7
nombre_elements = len(elements)
print(f"Nombre d'éléments sur la ligne 7 : {nombre_elements}")