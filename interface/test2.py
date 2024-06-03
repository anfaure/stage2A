import os
import math
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Fonction pour calculer ΔOD
def calculer_delta_OD(I0, I0bckg, I1, I1bckg):
    x = (I1 - I1bckg)
    delta_OD = 0 if x <= 0 else math.log10((I0 - I0bckg) / (I1 - I1bckg))
    return delta_OD

# Fonction pour charger le fichier
def charger_fichier():
    file_path = filedialog.askopenfilename()
    if file_path:
        chemin_entree.delete(0, tk.END)
        chemin_entree.insert(tk.END, file_path)

# Fonction pour exécuter le script
def executer_script():
    file_path = chemin_entree.get()
    if not os.path.isfile(file_path):
        messagebox.showerror("Erreur", "Le fichier n'existe pas. Veuillez entrer un chemin valide.")
        return

    try:
        longueur_donde_a_examiner = float(saisie_longueur_donde.get())
        nombre_scan = int(saisie_nombre_scan.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour la longueur d'onde et le nombre de scans.")
        return

    scans_a_examiner = []
    for i in range(nombre_scan):
        try:
            scan_num = int(saisies_scans[i].get()) - 1
            scans_a_examiner.append(scan_num)
        except ValueError:
            messagebox.showerror("Erreur", f"Le scan numéro {i+1} est invalide.")
            return

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
            delay.append(float(element[4]))
            for _ in range(5):
                next(f)
            ligne_courante = next(f)

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
        for _ in range(4):
            next(f)
        
        for i in range(scan_number):
            for _ in range(6):
                next(f)
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
        delta_OD = np.zeros((len(delay), len(longueurs_donde)))  # Créez une matrice 2D pour chaque scan
        for j in range(len(liste_I0[i])):
            for k in range(len(liste_I0[i][j])):
                delta_OD[j, k] = calculer_delta_OD(liste_I0[i][j][k], liste_I0bckg[i][k],
                                               liste_I1[i][j][k], liste_I1bckg[i][k])
        liste_delta_OD[i] = delta_OD

    # Trouver l'indice de la longueur d'onde correspondante
    try:
        indice_longueur_donde = longueurs_donde.index(longueur_donde_a_examiner)
    except ValueError:
        valeur_plus_proche = min(longueurs_donde, key=lambda x: abs(x - longueur_donde_a_examiner))
        indice_longueur_donde = longueurs_donde.index(valeur_plus_proche)

    # Extraire les valeurs de ΔOD pour la longueur d'onde spécifiée pour chaque scan
    delta_OD_a_examiner = []
    for scan_index in scans_a_examiner:
        scan = liste_delta_OD[scan_index]
        delta_OD_a_examiner.append([row[indice_longueur_donde] for row in scan])

    # Tracer le graphe
    for i, delta_OD in enumerate(delta_OD_a_examiner):
        plt.plot(delay, delta_OD, label=f'Scan {scans_a_examiner[i] + 1}')

    plt.xlabel('Delay (ns)')  # Titre abscisse
    plt.ylabel('ΔOD')  # Titre ordonnée
    plt.title(f"ΔOD en fonction du delay pour la longueur d'onde {valeur_plus_proche} nm ({longueur_donde_a_examiner})")  # Titre du graphe
    plt.legend()
    plt.grid(True)  # Afficher la grille
    plt.show()  # Afficher le graphe

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Analyse des données")

# Cadre pour le chemin du fichier
cadre_fichier = tk.Frame(fenetre)
cadre_fichier.pack(pady=10)

label_chemin = tk.Label(cadre_fichier, text="Chemin du fichier :")
label_chemin.grid(row=0, column=0)

chemin_entree = tk.Entry(cadre_fichier, width=50)
chemin_entree.grid(row=0, column=1, padx=10)

bouton_fichier = tk.Button(cadre_fichier, text="Parcourir", command=charger_fichier)
bouton_fichier.grid(row=0, column=2)

# Cadre pour la longueur d'onde à examiner
cadre_longueur_donde = tk.Frame(fenetre)
cadre_longueur_donde.pack(pady=10)

label_longueur_donde = tk.Label(cadre_longueur_donde, text="Longueur d'onde à examiner :")
label_longueur_donde.grid(row=0, column=0)

saisie_longueur_donde = tk.Entry(cadre_longueur_donde, width=10)
saisie_longueur_donde.grid(row=0, column=1, padx=10)

# Cadre pour le nombre de scans à examiner
cadre_nombre_scan = tk.Frame(fenetre)
cadre_nombre_scan.pack(pady=10)

label_nombre_scan = tk.Label(cadre_nombre_scan, text="Nombre de scans à examiner :")
label_nombre_scan.grid(row=0, column=0)

saisie_nombre_scan = tk.Entry(cadre_nombre_scan, width=10)
saisie_nombre_scan.grid(row=0, column=1, padx=10)

# Cadre pour les numéros de scans à examiner
cadre_scans = tk.Frame(fenetre)
cadre_scans.pack(pady=10)

label_scans = tk.Label(cadre_scans, text="Numéros des scans à examiner :")
label_scans.grid(row=0, column=0)

saisies_scans = []
for i in range(5):  # Maximum 5 scans
    saisie_scan = tk.Entry(cadre_scans, width=10)
    saisie_scan.grid(row=0, column=i+1, padx=5)
    saisies_scans.append(saisie_scan)

# Bouton pour exécuter le script
bouton_executer = tk.Button(fenetre, text="Exécuter", command=executer_script)
bouton_executer.pack(pady=10)

# Affichage de la fenêtre
fenetre.mainloop()