import math

def calculer_delta_OD(I1, I1bckg, I2, I2bckg):
    delta_OD = math.log10((I1 - I1bckg) / (I2 / I2bckg))
    return delta_OD

# Exemple d'utilisation du script avec des valeurs arbitraires
I1 = 100
I1bckg = 20
I2 = 50
I2bckg = 10

resultat = calculer_delta_OD(I1, I1bckg, I2, I2bckg)
print("Le résultat du calcul de delta OD est :", resultat)