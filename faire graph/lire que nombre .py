# Chemin du fichier à lire
file_path = '/home/anaelle/Cozy Drive/Stage IPR/scripts/faire graph/BYiG261022_TA_15.dat'

# Ouvrir le fichier en mode lecture
with open(file_path, 'r') as file:
    # Ignorer les 6 premières lignes
    for _ in range(3):
        next(file)
    # Lire la septième ligne
    line_4 = file.readline()

# Séparer la ligne en éléments en utilisant l'espace comme séparateur
elements = line_4.split()

# Liste pour stocker les valeurs numériques
valeurs_numeriques = []

# Boucle pour filtrer les valeurs numériques
for element in elements:
    if element.isdigit():
        valeurs_numeriques.append(float(element))  # Convertir la chaîne en nombre entier et l'ajouter à la liste

# Afficher les valeurs numériques
print("Valeurs numériques sur la ligne 4 :", valeurs_numeriques)