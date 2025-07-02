import numpy as np 

class SistemaExperto:
    def __init__(self):
        # 1. BASE DE CONOCIMIENTO DIFUSA
        # Umbrales para cada emoción (definen las funciones de membresía)
        self.umbrales = {
            'Feliz':       {'inicio': 0.36,  'max': 0.55},
            'Sorprendido': {'inicio': 0.10,  'max': 0.22},
            'Triste':      {'inicio': 0.005, 'max': 0.02},
            'Enfadado':    {'inicio': 0.018, 'max': 0.060},
            'Susto':       {'inicio': 0.11,  'max': 0.22},
        }
        # Valores numéricos para defuzzificación tipo centroide
        # -2        -1.5     -1       0       1        2
        # Enfadado  Susto   Triste  Neutral  Sorpr.   Feliz
        self.emocion_valores = {
            'Feliz': 2,
            'Sorprendido': 1,
            'Neutral': 0,
            'Triste': -1,
            'Enfadado': -2,
            'Susto': -1.5,
        }

    # 2. FUZZIFICACIÓN: Función de pertencia 
    def funcionDePertenencia(self, valor, umbralMin, umbralMax):
        """
        Función difusa tipo rampa:
        - 0 si valor <= inicio
        - 1 si valor >= max
        - valor proporcional entre inicio y max
        """
        if valor <= umbralMin:
            return 0.0
        elif valor >= umbralMax:
            return 1.0
        else:
            return (valor - umbralMin) / (umbralMax - umbralMin)

    # 3. PROCESAMIENTO Y ANÁLISIS DE EMOCIÓN
    def analizar_emocion(self, landmarks):
        """
        Analiza los landmarks faciales y devuelve:
         - El grado de pertenencia de cada emoción.
         - La emoción detectada mediante el método del centroide.
        Parámetros:
            - landmarks: lista de objetos con atributos .x y .y (MediaPipe)
        """

        # 3.1 ADQUISICIÓN Y PREPROCESAMIENTO DE DATOS CRISP
        def lm(idx): return [landmarks[idx].x, landmarks[idx].y]

        ancho_cara = np.linalg.norm(np.array(lm(234)) - np.array(lm(454)))

        # Boca
        comisura_izquierda = lm(61)
        comisura_derecha = lm(291)
        boca_arriba = lm(13)
        boca_abajo  = lm(14)

        # Ojos
        parpado_sup_izq    = lm(159)
        parpado_inf_izq    = lm(145)
        parpado_sup_dcha   = lm(386)
        parpado_inf_dcha   = lm(374)

        # Medidas Faciales (normalizadas)
        ancho_boca       = np.linalg.norm(np.array(comisura_izquierda) - np.array(comisura_derecha)) / ancho_cara
        apertura_boca    = np.linalg.norm(np.array(boca_arriba) - np.array(boca_abajo)) / ancho_cara
        apertura_ojo_izq = np.linalg.norm(np.array(parpado_sup_izq) - np.array(parpado_inf_izq)) / ancho_cara
        apertura_ojo_dcha = np.linalg.norm(np.array(parpado_sup_dcha) - np.array(parpado_inf_dcha)) / ancho_cara
        apertura_ojos    = (apertura_ojo_izq + apertura_ojo_dcha) / 2

        centro_boca_y       = (boca_arriba[1] + boca_abajo[1]) / 2
        centro_comisuras_y  = (comisura_izquierda[1] + comisura_derecha[1]) / 2
        caida_comisuras     = centro_comisuras_y - centro_boca_y
        fruncir_labios      = apertura_boca

        # 4. FUZZIFICACIÓN: Cálculo de grados de pertenencia
        emociones = {
            'Feliz':       self.funcionDePertenencia(ancho_boca, self.umbrales['Feliz']['inicio'], self.umbrales['Feliz']['max']),
            'Sorprendido': self.funcionDePertenencia(apertura_boca, self.umbrales['Sorprendido']['inicio'], self.umbrales['Sorprendido']['max']),
            'Triste':      self.funcionDePertenencia(caida_comisuras, self.umbrales['Triste']['inicio'], self.umbrales['Triste']['max']),
            'Enfadado':    self.funcionDePertenencia(fruncir_labios, self.umbrales['Enfadado']['inicio'], self.umbrales['Enfadado']['max']),
            'Susto':       self.funcionDePertenencia(apertura_ojos, self.umbrales['Susto']['inicio'], self.umbrales['Susto']['max']),
        }

        # Opcional: imprime los valores faciales para calibración
        print(f"mw: {ancho_boca:.3f} mo: {apertura_boca:.3f} ao: {apertura_ojos:.3f} cc: {caida_comisuras:.3f} fl: {fruncir_labios:.3f}")

        # 5. INFERENCIA Y AGREGACIÓN
        emociones['Neutral'] = 1.0 - max(emociones.values())

        # 6. DEFUZZIFICACIÓN (solo centroide)
        numerador = sum(emociones[k] * self.emocion_valores[k] for k in emociones)
        denominador = sum(emociones.values())
        centroide = numerador / denominador if denominador > 0 else 0
        detected = min(self.emocion_valores.keys(), key=lambda k: abs(self.emocion_valores[k] - centroide))

        return emociones, detected
