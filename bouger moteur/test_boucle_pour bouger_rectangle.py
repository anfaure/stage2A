# Définition de la largeur du déplacement
largeur = 4
hauteur = 8
hauteur_div_par_2 = int (hauteur / 2)
#hauteur_div_2 = hauteur / 2
# Position initiale de l'échantillon
x, y = 0, 0

# Boucle pour chaque mouvement
for _ in range(hauteur_div_par_2):
    # Mouvement vers la droite
    for i in range(largeur):
        x += 1
    
    # Mouvement vers le haut
    y += 1
    
    # Mouvement vers la gauche
    for i in range(largeur):
        x -= 1
        
    # Mouvement vers le haut
    y += 1
    