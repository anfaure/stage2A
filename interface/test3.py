import tkinter as tk
from tkinter import messagebox
import math

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
            self.canvas.coords(self.sample, 0, 0, 10, 10)  # Réinitialise la position à (0,0)
            self.move_sample()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour la hauteur, la largeur et la vitesse.")

    def move_sample(self):
        if self.in_arc:
            # Déplacer en arc de cercle
            self.x += self.direction * self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))
            self.angle += 5
            if self.angle >= 180:
                self.in_arc = False
                self.angle = 0
        else:
            # Déplacement linéaire
            if 0 <= self.x < self.width - 10:
                self.x += self.direction * self.speed
            elif self.x >= self.width - 10 or self.x < 0:
                self.in_arc = True
                self.direction = -self.direction
                self.x = max(min(self.x, self.width - 10), 0)
                self.y += self.speed
        
        self.canvas.coords(self.sample, self.x, self.y, self.x + 10, self.y + 10)
        self.root.update()
        self.canvas.after(50, self.move_sample)

if __name__ == "__main__":
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()
