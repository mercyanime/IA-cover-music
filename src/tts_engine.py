from TTS.api import TTS
from .utils import guardar_audio

class MotorTTS:
    def __init__(self, modelo="tts_models/es/mai/tacotron2-DDC"):
        self.modelo = TTS(modelo, progress_bar=False, gpu=False)

    def generar_voz(self, texto, ruta_salida):
        if not texto.strip():
            raise ValueError("El texto no puede estar vacío")
        
        self.modelo.tts_to_file(text=texto, file_path=ruta_salida)
        print(f"✅ Voz base generada: {ruta_salida}")
        return ruta_salida
