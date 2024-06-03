import tkinter as tk
from tkinter import messagebox
import time
import sys
from lightcon.harpia import Harpia

class SampleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contrôler l'échantillon")

        # Labels et champs de saisie pour la hauteur
        self.height_label = tk.Label(root, text="Hauteur :")
        self.height_label.pack(pady=5)
        self.height_entry = tk.Entry(root)
        self.height_entry.pack(pady=5)

        # Labels et champs de saisie pour la largeur
        self.width_label = tk.Label(root, text="Largeur :")
        self.width_label.pack(pady=5)
        self.width_entry = tk.Entry(root)
        self.width_entry.pack(pady=5)
        
        # Labels et champs de saisie pour la vitesse
        self.speed_label = tk.Label(root, text="Vitesse (pixels par mouvement) :")
        self.speed_label.pack(pady=5)
        self.speed_entry = tk.Entry(root)
        self.speed_entry.pack(pady=5)

        # Bouton pour démarrer le mouvement
        self.start_button = tk.Button(root, text="Démarrer", command=self.start_movement)
        self.start_button.pack(pady=20)

        # Canvas pour dessiner l'échantillon
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(pady=20)

        # Variables pour le mouvement
        self.speed = 0
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.direction = 0
        self.angle = 0
        self.in_arc = False
        self.arc_reverse = False

    def start_movement(self):
        try:
            self.height = int(self.height_entry.get()) * 100
            self.width = int(self.width_entry.get()) * 100
            self.speed = float(self.speed_entry.get())

            # Mettre à jour la taille du canvas
            self.canvas.config(width=self.width, height=self.height)

            # Créer un point de taille 10x10
            self.canvas.delete("all")
            self.sample = self.canvas.create_rectangle(0, 0, 10, 10, fill="#f074dd")

            # Réinitialiser la position du point
            self.x, self.y = 0, 0
            self.direction = 1  # 1 pour droite, -1 pour gauche
            self.angle = 0
            self.in_arc = False
            self.arc_reverse = False
            self.canvas.coords(self.sample, 0, 0, 10, 10)  # Réinitialise la position à (0,0)

            # Initialiser Harpia
            self.harpia = Harpia('127.0.0.1')
            if not self.harpia.connected:
                messagebox.showerror("Erreur", "Impossible de se connecter à Harpia")
                return
            self.harpia.chopper_start()
            self.harpia.sample_mover_go_to_zero()
            self.harpia.set_sample_mover_velocity(self.speed)
            
            self.move_sample()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour la hauteur, la largeur et la vitesse.")

    def move_sample(self):
        try:
            for _ in range(int(self.height / 200)):
                for _ in range(int(self.width / 100)):
                    self.x += 1
                    self.update_position()
                    time.sleep(2) # Pour attendre que le mouvement se réalise
                self.harpia.set_target_rotate_angle(self.angle)
                self.y += 1
                self.update_position()
                time.sleep(2) # Pour attendre que le mouvement se réalise
                for _ in range(int(self.width / 100)):
                    self.x -= 1
                    self.update_position()
                    time.sleep(2) # Pour attendre que le mouvement se réalise
                self.harpia.set_target_rotate_angle(self.angle)
                self.y += 1
                self.update_position()
                time.sleep(2) # Pour attendre que le mouvement se réalise

            for _ in range(int(self.width / 100)):
                self.x += 1
                self.update_position()
                time.sleep(2) # Pour attendre que le mouvement se réalise
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def update_position(self):
        self.harpia.sample_mover_go_to_xy_and_wait_stop(self.x, self.y)
        self.canvas.coords(self.sample, self.x, self.y, self.x + 10, self.y + 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()