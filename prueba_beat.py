import os
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment, effects

# ---------------- CONFIGURACIÓN ----------------
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

CARPETA_SALIDAS = os.path.join("assets", "salidas")
os.makedirs(CARPETA_SALIDAS, exist_ok=True)

# ---------------- FUNCIÓN DE BEAT MEJORADA ----------------
def generar_beat(estilo="Trap latino", duracion_seg=30, ruta_salida="beat_prueba.wav"):
    sr = 22050  # Frecuencia estándar
    t = np.linspace(0, duracion_seg, int(sr * duracion_seg), endpoint=False)

    # BPM según estilo
    if "balada" in estilo.lower():
        bpm = 72
    elif "regueton" in estilo.lower() or "rápido" in estilo.lower():
        bpm = 105
    elif "trap" in estilo.lower():
        bpm = 92
    else:
        bpm = 90

    duracion_compas = 60 / bpm
    muestras_compas = int(sr * duracion_compas)

    # 🔊 BAJO FUERTE Y CONSTANTE
    frec_bajo = 55
    onda_bajo = 0.32 * np.sin(2 * np.pi * frec_bajo * t)
    envolvente = 0.75 + 0.25 * np.sin(2 * np.pi * 0.4 * t)
    bajo = onda_bajo * envolvente

    # 🥁 BATERÍA CON RITMO MARCADO
    bateria = np.zeros_like(t)
    golpes_por_compas = [0, int(muestras_compas * 0.5)]  # Tiempos 1 y 3

    for compas in range(int(duracion_seg / duracion_compas)):
        inicio_compas = compas * muestras_compas
        for golpe in golpes_por_compas:
            pos = inicio_compas + golpe
            if pos + int(sr * 0.06) < len(t):
                bateria[pos : pos + int(sr * 0.06)] = 0.85

    # 🎵 MEZCLA Y AJUSTE
    beat = bajo + bateria * 0.28
    beat = np.clip(beat, -1.0, 1.0)  # Evitar distorsión
    beat = beat * 0.92  # Nivel de volumen seguro

    # Guardar como WAV
    wavfile.write(ruta_salida, sr, (beat * 32767).astype(np.int16))

    # Mejorar calidad final
    audio = AudioSegment.from_wav(ruta_salida)
    audio = effects.normalize(audio)
    audio.export(ruta_salida, format="wav", bitrate="192k")

    print(f"✅ Beat generado correctamente en: {ruta_salida}")
    return True

# ---------------- PRUEBA ----------------
if __name__ == "__main__":
    print("🎹 Generando beat de prueba...")
    generar_beat(estilo="Trap latino", duracion_seg=30, ruta_salida=os.path.join(CARPETA_SALIDAS, "beat_prueba.wav"))
    print("🏁 Proceso terminado.")
