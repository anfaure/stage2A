import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Données de longueurs d'onde, délai et deltaOD (exemple)
longueurs_donde = [400, 450, 500, 550, 600]  # Exemple de longueurs d'onde
delais = [0, 1, 2, 3, 4]  # Exemple de délais
deltaOD = [
    [1, 2, 3, 4, 5],  # Exemple de deltaOD pour le premier délai
    [2, 3, 4, 5, 6],  # Exemple de deltaOD pour le deuxième délai
    [3, 4, 5, 6, 7],  # Exemple de deltaOD pour le troisième délai
    [4, 5, 6, 7, 8],  # Exemple de deltaOD pour le quatrième délai
    [5, 6, 7, 8, 9],  # Exemple de deltaOD pour le cinquième délai
]

# Création de la figure et des axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Création du maillage pour les longueurs d'onde et les délais
X, Y = plt.meshgrid(longueurs_donde, delais)

# Tracer le graphique 3D
for i in range(len(delais)):
    ax.plot_wireframe(X, Y[i], deltaOD[i], label=f'Délai {delais[i]}')

# Étiquetage des axes
ax.set_xlabel('Longueurs d\'onde')
ax.set_ylabel('Délai')
ax.set_zlabel('DeltaOD')

# Afficher la légende
ax.legend()

# Afficher le graphique
plt.show()