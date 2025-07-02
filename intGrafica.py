import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

class IntGrafica:
    def __init__(self, controlador):
        self.controlador = controlador
        self.root = tk.Tk()
        self.root.title("Análisis de emociones en tiempo real")
        self.root.geometry("900x600")
        self.root.configure(bg="#222")
        self.progresoxEmocion = {}
        self.crearInterfaz()

    def crearInterfaz(self):
        pantallaPrincipal = tk.Frame(self.root, bg="#222")
        pantallaPrincipal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        videoPaginaPrincipal = tk.Frame(pantallaPrincipal, bg="#222")
        videoPaginaPrincipal.pack(side=tk.LEFT, padx=10, pady=10)

        self.label_video = tk.Label(videoPaginaPrincipal, bg="#111")
        self.label_video.pack(pady=10)

        self.label_estado = tk.Label(videoPaginaPrincipal, text="Estado: Inactivo", font=("Arial", 16), fg="#eee", bg="#222")
        self.label_estado.pack(pady=8)

        zonaBotones = tk.Frame(videoPaginaPrincipal, bg="#222")
        zonaBotones.pack(pady=8)

        self.btn_iniciar = ttk.Button(zonaBotones, text="Iniciar", width=13, command=self.controlador.iniciar)
        self.btn_detener = ttk.Button(zonaBotones, text="Detener", width=13, state="disabled", command=self.controlador.detener)
        self.btn_dashboard = ttk.Button(zonaBotones, text="Ver Proceso", width=16, state="disabled", command=self.controlador.ver_dashboard)

        self.btn_iniciar.grid(row=0, column=0, padx=6)
        self.btn_detener.grid(row=0, column=1, padx=6)
        self.btn_dashboard.grid(row=0, column=2, padx=6)

        emocionesPaginaPrincipal = tk.Frame(pantallaPrincipal, bg="#222")
        emocionesPaginaPrincipal.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(emocionesPaginaPrincipal, text="Emociones Detectadas", font=("Arial", 17, "bold"), fg="#1e90ff", bg="#222").pack(pady=7)

        for emocion in ['Feliz', 'Sorprendido', 'Susto', 'Triste', 'Enfadado', 'Neutral']:
            f = tk.Frame(emocionesPaginaPrincipal, bg="#222")
            f.pack(fill=tk.X, padx=12, pady=3)
            l = tk.Label(f, text=emocion, width=12, anchor="w", fg="#eee", bg="#222", font=("Arial", 12, "bold"))
            l.pack(side=tk.LEFT)
            pb = ttk.Progressbar(f, length=270, mode="determinate")
            pb.pack(side=tk.LEFT, padx=10)
            self.progresoxEmocion[emocion] = pb

    def actualizar_estado(self, texto, color):
        self.label_estado.config(text=texto, fg=color)

    def mostrar_frame(self, frame, emocion_actual):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((420, 320))
        imgtk = ImageTk.PhotoImage(image=img)
        self.label_video.imgtk = imgtk
        self.label_video.config(image=imgtk)
        self.actualizar_estado(f"Expresión detectada: {emocion_actual}", "#1e90ff")

    def actualizar_barras(self, emociones):
        for emocion, val in emociones.items():
            self.progresoxEmocion[emocion]['value'] = int(val * 100)

    def mostrar_dashboard(self, historial):
        paginaDashboard = tk.Toplevel(self.root)
        paginaDashboard.title("Dashboard de emociones")
        paginaDashboard.geometry("820x420")
        emociones_lista = [e for t, e in historial]
        total = len(emociones_lista)
        contadorEmociones = Counter(emociones_lista)
        emociones = list(contadorEmociones.keys())
        totalxEmocion = [contadorEmociones[e] / total for e in emociones]
        fig, axs = plt.subplots(1, 2, figsize=(9, 4))
        axs[0].pie(totalxEmocion, labels=emociones, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.5))
        axs[0].set_title('Porcentaje de tiempo por emoción')
        tiempos = [t - historial[0][0] for t, e in historial]
        emocion_idx = [emociones.index(e) for t, e in historial]
        axs[1].plot(tiempos, emocion_idx, drawstyle='steps-post')
        axs[1].set_yticks(range(len(emociones)))
        axs[1].set_yticklabels(emociones)
        axs[1].set_xlabel('Tiempo (s)')
        axs[1].set_title('Evolución de emociones')
        axs[1].grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=paginaDashboard)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def iniciar_mainloop(self):
        self.root.mainloop()      