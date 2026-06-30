from .utils import cargar_audio, guardar_audio, ajustar_velocidad
import librosa

class SincronizadorRitmo:
    def __init__(self, bpm_objetivo=133):
        self.bpm_objetivo = bpm_objetivo

    def detectar_bpm(self, señal, sr):
        tempo, _ = librosa.beat.beat_track(y=señal, sr=sr)
        return float(tempo)

    def ajustar_a_bpm(self, ruta_entrada, ruta_salida):
        señal, sr = cargar_audio(ruta_entrada)
        bpm_actual = self.detectar_bpm(señal, sr)

        if bpm_actual <= 0:
            factor = 1.0
        else:
            factor = self.bpm_objetivo / bpm_actual

        señal_ajustada = ajustar_velocidad(señal, factor)
        guardar_audio(señal_ajustada, ruta_salida, sr)
        print(f"✅ Ritmo ajustado a {self.bpm_objetivo} BPM")
        return ruta_salida
