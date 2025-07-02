# Trabajo Fin de Grado Antonio Carrasco Juárez

**Análisis de Emociones en Tiempo Real usando Visión Artificial y un Sistema Experto Difuso**

Este proyecto es una aplicación desarrollada en Python que analiza emociones faciales en tiempo real usando la webcam del sistema. Combina técnicas de visión artificial, una base de conocimiento difusa y una interfaz gráfica interactiva para visualizar la evolución de emociones detectadas.

## Características principales

- **Captura de video** en tiempo real desde la webcam.
- **Procesamiento de landmarks faciales** usando MediaPipe.
- **Sistema experto difuso** para clasificación de emociones (feliz, sorprendido, triste, enfadado, susto, neutral).
- **Interfaz gráfica** intuitiva con barras de progreso y dashboard de análisis histórico.
- **Visualización de estadísticas** de emociones en gráficos interactivos.

## Requisitos

- Python 3.8+
- Webcam compatible

## Instalación y uso

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/anthonycaju7/TFG-ACJ.git
    cd TFG-ACJ
    ```

2. **(Opcional pero recomendado) Crea un entorno virtual:**

    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En Linux/Mac
    source venv/bin/activate
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```
4. **Ejecuta la aplicación:**

    ```bash
    python main.py
    ```

Se abrirá una ventana gráfica donde podrás:

- Pulsar **Iniciar** para comenzar el análisis en tiempo real.
- Pulsar **Detener** para finalizar.
- Pulsar **Ver Proceso** para ver el dashboard de la sesión actual.

---

## Estructura principal del proyecto

- `main.py` — Entrada principal, lanza la interfaz gráfica.
- `controlador.py` — Lógica central: conecta captura de video, sistema experto y GUI.
- `captura_video.py` — Manejo de la webcam.
- `sistemaExperto.py` — Algoritmo difuso para clasificación de emociones.
- `intGrafica.py` — Interfaz gráfica y visualización de datos.
- `requirements.txt` — Lista de dependencias.

## Notas técnicas

- Usa [MediaPipe](https://google.github.io/mediapipe/) para detección de puntos faciales.
- La interfaz se desarrolla con `tkinter` y gráficos con `matplotlib`.
- Código listo para ser extendido o adaptado a nuevos modelos o más emociones.

## Autor

Antonio Carrasco Juárez 
Proyecto TFG - Universidad  
