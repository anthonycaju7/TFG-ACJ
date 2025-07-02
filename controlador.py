import time
from captura_video import CapturaVideo
from vision_Artificial import VisionArtificial
from sistemaExperto import SistemaExperto
from intGrafica import IntGrafica

class Controlador:
    """
    Clase que coordina todos los módulos del sistema: captura de vídeo, análisis de emociones,
    visión artificial y la interfaz gráfica.
    """
    def __init__(self):
        """
        Inicializa los módulos principales y variables de estado.
        """
        self.captura = CapturaVideo()            # Objeto para gestionar la webcam (abre al crear)
        self.vision = VisionArtificial()         # Objeto para detectar landmarks
        self.experto = SistemaExperto()          # Objeto para analizar emociones
        self.historial = []                      # Historial de emociones detectadas [(timestamp, emocion)]
        self.en_ejecucion = False                # Bandera de estado del análisis
        self.emocion_detectada = "Neutral"       # Emoción detectada actual
        self.int_grafica = IntGrafica(self)      # Interfaz gráfica, recibe referencia al controlador

    def iniciar(self):
        """
        Inicia la captura y análisis de vídeo, actualiza la interfaz y prepara el sistema.
        """
        # La cámara ya está abierta en el constructor, no hace falta iniciar
        self.en_ejecucion = True
        self.historial = []
        self.int_grafica.actualizar_estado("Estado: Analizando...", "#3bc463")
        self.int_grafica.btn_iniciar.config(state="disabled")
        self.int_grafica.btn_detener.config(state="normal")
        self.int_grafica.btn_dashboard.config(state="disabled")
        self.actualizar_frame()

    def detener(self):
        """
        Detiene el análisis. Actualiza el estado de la interfaz.
        """
        self.en_ejecucion = False
        # No hace falta liberar la cámara, se gestiona automáticamente
        self.int_grafica.actualizar_estado("Estado: Inactivo", "#e34234")
        self.int_grafica.btn_iniciar.config(state="normal")
        self.int_grafica.btn_detener.config(state="disabled")
        if self.historial:
            self.int_grafica.btn_dashboard.config(state="normal")

    def actualizar_frame(self):
        """
        Toma un frame, lo procesa, actualiza emociones y refresca la interfaz.
        Es llamada de forma recursiva por Tkinter usando after().
        """
        if not self.en_ejecucion:
            return

        fotograma = self.captura.obtener_frame()
        if fotograma is None:
            self.int_grafica.root.after(25, self.actualizar_frame)
            return

        puntos_faciales = self.vision.detectar_landmarks(fotograma)
        emociones = {}
        self.emocion_detectada = "Neutral"

        if puntos_faciales is not None:
            emociones, self.emocion_detectada = self.experto.analizar_emocion(puntos_faciales)
            self.int_grafica.actualizar_barras(emociones)
            self.historial.append((time.time(), self.emocion_detectada))

        self.int_grafica.mostrar_frame(fotograma, self.emocion_detectada)
        self.int_grafica.root.after(20, self.actualizar_frame)

    def ver_dashboard(self):
        """
        Muestra el dashboard con la evolución de emociones, si hay historial.
        """
        if self.historial:
            self.int_grafica.mostrar_dashboard(self.historial)
