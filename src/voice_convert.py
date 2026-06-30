from .utils import cargar_audio, guardar_audio, cambiar_tono

class ConvertidorVoz:
    def __init__(self, ruta_modelo=None, ruta_index=None):
        self.ruta_modelo = ruta_modelo
        self.ruta_index = ruta_index

    def aplicar_estilo_rap(self, ruta_entrada, ruta_salida, semitonos=2):
        señal, sr = cargar_audio(ruta_entrada)
        
        # Ajuste para voz grave y con fuerza
        señal = cambiar_tono(señal, sr, semitonos=-semitonos)
        señal = librosa.effects.preemphasis(señal, coef=0.95)

        guardar_audio(señal, ruta_salida, sr)
        print("✅ Estilo de voz aplicado: Rap agresivo")
        return ruta_salida
