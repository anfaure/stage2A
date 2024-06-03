import os
import math
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np

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
        afficher_cases_a_cocher(file_path)

# Fonction pour afficher les cases à cocher
def afficher_cases_a_cocher(file_path):
    # Lire le nombre de scans dans le fichier
    with open(file_path, 'r') as file:
        lines = file.readlines()
    scan_numbers = [int(re.search(r"scan (\d+)", line).group(1)) for line in lines if re.search(r"scan (\d+)", line)]
    scan_number = max(scan_numbers, default=0)
    
    # Supprimer les cases à cocher existantes
    for widget in cadre_scans.winfo_children():
        widget.destroy()
    
    # Créer les cases à cocher pour les scans
    global cases_a_cocher
    cases_a_cocher = []
    for i in range(scan_number):
        var = tk.BooleanVar()
        case = tk.Checkbutton(cadre_scans, text=f'Scan {i+1}', variable=var)
        case.grid(row=i//5, column=i%5, padx=5, pady=5)
        cases_a_cocher.append((i+1, var))

# Fonction pour lire une ligne en toute sécurité
def lire_ligne_securisee(f):
    try:
        return next(f)
    except StopIteration:
        return None

# Fonction pour exécuter le script
def executer_script():
    file_path = chemin_entree.get()
    if not os.path.isfile(file_path):
        messagebox.showerror("Erreur", "Le fichier n'existe pas. Veuillez entrer un chemin valide.")
        return

    try:
        longueur_donde_a_examiner = float(saisie_longueur_donde.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique valide pour la longueur d'onde.")
        return

    scans_a_examiner = [num for num, var in cases_a_cocher if var.get()]
    if not scans_a_examiner:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins un scan.")
        return

    # Lire les longueurs d'onde
    with open(file_path, 'r') as f:
        for _ in range(3):  # Ignorer les 3 premières lignes
            lire_ligne_securisee(f)
        quatrieme_ligne = lire_ligne_securisee(f)  # Lecture de la quatrième ligne (longueurs d'onde)
        if quatrieme_ligne is None:
            messagebox.showerror("Erreur", "Le fichier est trop court.")
            return
        longueurs_donde = quatrieme_ligne.split()[1:]  # Séparation de la ligne en une liste de chaînes de caractères
        longueurs_donde = [float(x) for x in longueurs_donde]  # Conversion en float

    # Lire les délais
    delay = []
    with open(file_path, 'r') as f:
        for _ in range(10):
            lire_ligne_securisee(f)
        ligne_courante = lire_ligne_securisee(f)
        while ligne_courante and "scan 1" in ligne_courante:  # tant qu'il y a scan 1 sur la ligne il exécute la boucle
            element = ligne_courante.split()
            delay.append(float(element[4]))
            for _ in range(5):
                lire_ligne_securisee(f)
            ligne_courante = lire_ligne_securisee(f)

    if not delay:
        messagebox.showerror("Erreur", "Aucun délai trouvé dans le fichier.")
        return

    # Récupérer le nombre de scans
    with open(file_path, 'r') as file:
        lines = file.readlines()
    scan_numbers = sorted(set(int(re.search(r"scan (\d+)", line).group(1)) for line in lines if re.search(r"scan (\d+)", line)))
    scan_number = max(scan_numbers, default=0)

    # Initialiser les listes pour les valeurs
    liste_I0bckg = [[] for _ in range(scan_number)]
    liste_I1bckg = [[] for _ in range(scan_number)]
    liste_I0 = [[] for _ in range(scan_number)]
    liste_I1 = [[] for _ in range(scan_number)]

    # Lire les données des fichiers et remplir les listes
    for i in range(scan_number):
        with open(file_path, 'r') as f:
            for _ in range(4 + (i * len(delay)*6)):  # Ignorer les lignes avant le scan
                lire_ligne_securisee(f)
            for _ in range(3): 
                lire_ligne_securisee(f)
            ligne_I1bckg = lire_ligne_securisee(f)
            ligne_I0bckg = lire_ligne_securisee(f)
            if ligne_I1bckg is None or ligne_I0bckg is None:
                messagebox.showerror("Erreur", "Le fichier est incomplet ou mal formé.")
                return
            I1bckg = [float(x) for x in ligne_I1bckg.split()]  # Lecture de la ligne I1bckg et conversion en float
            I0bckg = [float(x) for x in ligne_I0bckg.split()]  # Lecture de la ligne I0bckg et conversion en float
            liste_I1bckg[i] = I1bckg
            liste_I0bckg[i] = I0bckg

    # Lire les données de I0 et I1
    with open(file_path, 'r') as f:
        for _ in range(4):
            lire_ligne_securisee(f)
        
        for i in range(scan_number):
            for _ in range(6):
                lire_ligne_securisee(f)
            I0_scan = []
            I1_scan = []
            for j in range(len(delay)):
                for _ in range(3):  # Sauter 3 lignes
                    lire_ligne_securisee(f)

                # Lire les données de I1
                ligne_courante = lire_ligne_securisee(f)
                if ligne_courante is None:
                    break
                I1 = [float(x) for x in ligne_courante.split()]

                # Lire les données de I0
                ligne_courante = lire_ligne_securisee(f)
                if ligne_courante is None:
                    break
                I0 = [float(x) for x in ligne_courante.split()]
                lire_ligne_securisee(f)
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
        scan = liste_delta_OD[scan_index - 1]
        delta_OD_a_examiner.append([row[indice_longueur_donde] for row in scan])

    # Tracer le graphe
    for i, delta_OD in enumerate(delta_OD_a_examiner):
        plt.plot(delay, delta_OD, label=f'Scan {scans_a_examiner[i]}')

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

# Cadre pour les scans à examiner
cadre_scans = tk.Frame(fenetre)
cadre_scans.pack(pady=10)

# Bouton pour exécuter le script
bouton_executer = tk.Button(fenetre, text="Exécuter", command=executer_script)
bouton_executer.pack(pady=10)

# Affichage de la fenêtre
fenetre.mainloop()
