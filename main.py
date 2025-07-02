from controlador import Controlador  # Importa la clase principal del sistema

if __name__ == "__main__":
    # Si este archivo es el principal (no un import), lanza la aplicación
    controlador = Controlador()                 # Crea la instancia que coordina todo el sistema
    controlador.int_grafica.iniciar_mainloop()  # Inicia el bucle principal de la interfaz gráfica
