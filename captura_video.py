import cv2
class CapturaVideo:
     # Constructor para poder usar la cámara del sitema
     def __init__(self):
          self.camara = cv2.VideoCapture(0) # Camara principal del sistema 0
          if not self.camara.isOpened():
               raise RuntimeError("no se puedo abrir la cámara")
    
     def obtener_frame(self):
       if self.camara.isOpened():
          captura, frame = self.camara.read()
          if captura:
               return frame
          return None
    
        # Método opcional para verificar si la cámara está abierta y evtiar errores.
     def esta_abierta(self):
        return self.camara.isOpened()

    # Destructor: libera la cámara automáticamente al destruir el objeto
     def __del__(self):
        if self.camara and self.camara.isOpened():
            self.camara.release()
