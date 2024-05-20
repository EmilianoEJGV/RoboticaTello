import tkinter as tk
from tkinter import Label, ttk, Canvas
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from SeguimientoFacial import SeguimientoFacial
import cv2


class DroneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control del Dron")
        self.root.geometry("800x600")

        self.drone_control = SeguimientoFacial()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12))

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configuración del grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)

        # Video en el centro
        self.video_label = Label(self.frame)
        self.video_label.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        # Botones a la izquierda
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.takeoff_button = ttk.Button(self.buttons_frame, text="Despegar", command=self.takeoff, style="TButton")
        self.takeoff_button.pack(pady=5)

        self.land_button = ttk.Button(self.buttons_frame, text="Aterrizar", command=self.land, style="TButton")
        self.land_button.pack(pady=5)

        # Batería a la derecha
        self.battery_frame = ttk.Frame(self.frame)
        self.battery_frame.grid(row=0, column=2, pady=10, padx=10, sticky="n")

        self.battery_label = ttk.Label(self.battery_frame, text="Batería", style="TLabel")
        self.battery_label.pack(pady=5)

        self.battery_canvas = Canvas(self.battery_frame, width=50, height=150, bg="white")
        self.battery_canvas.pack(pady=10)

        # Iniciar la actualización del video y de la batería
        self.update_frame()
        self.update_battery()

    def takeoff(self):
        self.drone_control.takeoff()

    def land(self):
        self.drone_control.land()

    def update_frame(self):
        img = self.drone_control.get_frame()
        img = cv2.resize(img, (self.drone_control.w, self.drone_control.h))
        img, info = self.drone_control.find_my_face(img)
        self.drone_control.sigue_cara(info)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.video_label.after(10, self.update_frame)

    def update_battery(self):
        battery = self.drone_control.get_battery()
        self.draw_battery(battery)
        self.root.after(5000, self.update_battery)

    def draw_battery(self, battery):
        self.battery_canvas.delete("all")
        self.battery_canvas.create_rectangle(10, 10, 40, 140, outline="black", width=2)
        fill_height = 130 * (battery / 100)
        fill_color = "red" if battery < 20 else "green"
        self.battery_canvas.create_rectangle(10, 140 - fill_height, 40, 140, fill=fill_color)
        self.battery_canvas.create_text(25, 75, text=f"{battery}%", font=("Helvetica", 12), fill="black")


if __name__ == '__main__':
    root = ThemedTk(theme="arc")
    app = DroneApp(root)
    root.mainloop()
