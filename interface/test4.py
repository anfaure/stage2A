import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrajectoryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Trajectory App")

        # Frame pour le panneau de contrôle
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, padx=10, pady=10)

        # Labels pour la position actuelle
        ttk.Label(control_frame, text="Position actuelle:").grid(row=1, column=0, sticky='W')
        self.actual_x = ttk.Label(control_frame, text="1.000")
        self.actual_x.grid(row=1, column=1)
        self.actual_y = ttk.Label(control_frame, text="0.000")
        self.actual_y.grid(row=1, column=2)

        # Canvas pour le graphique
        self.figure, self.ax = plt.subplots()
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 8)
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=1)

        # Boutons de contrôle
        self.create_control_buttons(control_frame)

        # Bouton de démarrage
        ttk.Button(control_frame, text="DÉMARRER", command=self.start_trajectory).grid(row=5, column=0, columnspan=3)

        # Initialiser la liste pour stocker les points de la trajectoire
        self.trajectory = [(1, 0)]  # Début à (1, 0)
        self.draw_trajectory()

        # Liste pour suivre les mouvements
        self.movement_sequence = []

    def create_control_buttons(self, parent):
        # Boutons de direction
        arrows_frame = ttk.Frame(parent)
        arrows_frame.grid(row=2, column=0, columnspan=3)

        ttk.Button(arrows_frame, text="↑", command=lambda: self.move(0, 1)).grid(row=0, column=1)
        ttk.Button(arrows_frame, text="←", command=lambda: self.move(-1, 0)).grid(row=1, column=0)
        ttk.Button(arrows_frame, text="○", command=self.reset_position).grid(row=1, column=1)
        ttk.Button(arrows_frame, text="→", command=lambda: self.move(1, 0)).grid(row=1, column=2)
        ttk.Button(arrows_frame, text="↓", command=lambda: self.move(0, -1)).grid(row=2, column=1)

        # Contrôle de la vitesse
        ttk.Label(parent, text="Vitesse:").grid(row=3, column=0, sticky='W')
        self.speed = ttk.Scale(parent, from_=1, to=10, orient='horizontal')
        self.speed.grid(row=3, column=1, columnspan=2)

        # Contrôle de la grille
        ttk.Label(parent, text="Grille:").grid(row=4, column=0, sticky='W')
        self.grid_on = tk.BooleanVar()
        ttk.Checkbutton(parent, variable=self.grid_on, command=self.toggle_grid).grid(row=4, column=1, columnspan=2)

    def move(self, dx, dy):
        current_x = float(self.actual_x.cget("text"))
        current_y = float(self.actual_y.cget("text"))
        new_x = current_x + dx
        new_y = current_y + dy
        self.update_position(new_x, new_y)

        # Enregistrer le mouvement
        self.movement_sequence.append((dx, dy))
        self.check_special_sequence()

    def update_position(self, x, y):
        self.actual_x.config(text=f"{x:.3f}")
        self.actual_y.config(text=f"{y:.3f}")
        self.trajectory.append((x, y))
        self.draw_trajectory()

    def draw_trajectory(self):
        self.ax.clear()
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 8)
        self.ax.grid(self.grid_on.get())

        if len(self.trajectory) > 1:
            x_coords, y_coords = zip(*self.trajectory)
            self.ax.plot(x_coords, y_coords, marker='o')
        else:
            x, y = self.trajectory[0]
            self.ax.plot(x, y, marker='o')
        
        self.canvas.draw()

    def reset_position(self):
        self.trajectory = [(1, 0)]  # Réinitialise à (1, 0)
        self.update_position(1, 0)
        self.movement_sequence = []

    def start_trajectory(self):
        target_x = float(self.target_x.get())
        target_y = float(self.target_y.get())
        self.update_position(target_x, target_y)

    def toggle_grid(self):
        self.ax.grid(self.grid_on.get())
        self.canvas.draw()

    def check_special_sequence(self):
        if len(self.movement_sequence) >= 3:
            if (self.movement_sequence[-3] == (1, 0) and
                self.movement_sequence[-2] == (1, 0) and
                self.movement_sequence[-1] == (0, 1)):
                self.draw_semicircle('right')
            elif (self.movement_sequence[-3] == (-1, 0) and
                self.movement_sequence[-2] == (-1, 0) and
                self.movement_sequence[-1] == (0, 1)):
                self.draw_semicircle('left')
            elif (self.movement_sequence[-3] == (0, 1) and
                self.movement_sequence[-2] == (0, 1) and
                self.movement_sequence[-1] == (1, 0)):
                self.draw_semicircle('up')
            elif (self.movement_sequence[-3] == (0, -1) and
                self.movement_sequence[-2] == (0, -1) and
                self.movement_sequence[-1] == (1, 0)):
                self.draw_semicircle('down')

    def draw_semicircle(self, direction):
        valy = float(self.actual_y.cget("text"))
        valx = float(self.actual_x.cget("text"))
        radius = 0.5

        if direction == 'right':
            center_x, center_y = valx, valy - 0.5
            theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
            x = center_x + radius * np.cos(theta)
            y = center_y + radius * np.sin(theta)
        elif direction == 'left':
            center_x, center_y = valx, valy - 0.5
            theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
            x = center_x - radius * np.cos(theta)
            y = center_y + radius * np.sin(theta)
        elif direction == 'up':
            center_x, center_y = valx - 0.5, valy
            theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
            x = center_x + radius * np.sin(theta)
            y = center_y + radius * np.cos(theta)
        elif direction == 'down':
            center_x, center_y = valx - 0.5, valy
            theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
            x = center_x + radius * np.sin(theta)
            y = center_y - radius * np.cos(theta)

        self.ax.plot(x, y, color='b')
        self.trajectory.extend([(None, None)] + list(zip(x, y)))  # Ajouter un point de discontinuité
        self.canvas.draw()

if __name__ == "__main__":
    app = TrajectoryApp()
    app.mainloop()