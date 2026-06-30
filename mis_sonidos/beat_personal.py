import os
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment, effects

# ---------------- CONFIGURACIÓN ----------------
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

CARPETA_SALIDAS = os.path.join("assets", "salidas")
CARPETA_SONIDOS = os.path.join("mis_sonidos")

os.makedirs(CARPETA_SALIDAS, exist_ok=True)
os.makedirs(CARPETA_SONIDOS, exist_ok=True)

# ---------------- FUNCIÓN PARA CARGAR TUS SONIDOS ----------------
def cargar_sonido(ruta, duracion_max=1.0):
    """Carga un archivo de sonido y lo normaliza"""
    try:
        audio = AudioSegment.from_file(ruta)
        audio = audio.set_frame_rate(22050).set_channels(1)
        audio = effects.normalize(audio, headroom=-2.0)
        # Cortar si es muy largo
        if len(audio) > duracion_max * 1000:
            audio = audio[:int(duracion_max * 1000)]
        return np.array(audio.get_array_of_samples(), dtype=np.float32) / 32767.0
    except:
        return None

# ---------------- GENERAR BEAT USANDO TUS SONIDOS ----------------
def generar_beat_con_tus_sonidos(estilo="Trap latino", duracion_seg=30, ruta_salida="beat_personalizado.wav"):
    sr = 22050
    duracion_seg = max(duracion_seg, 10)
    total_muestras = int(sr * duracion_seg)
    beat = np.zeros(total_muestras, dtype=np.float32)

    # BPM según estilo
    if "balada" in estilo.lower():
        bpm = 72
    elif "regueton" in estilo.lower():
        bpm = 105
    elif "trap" in estilo.lower():
        bpm = 90
    else:
        bpm = 88

    duracion_compas = 60 / bpm
    muestras_compas = int(sr * duracion_compas)

    # 🎯 BUSCAR TUS SONIDOS EN LA CARPETA
    archivos = [f for f in os.listdir(CARPETA_SONIDOS) if f.lower().endswith((".wav", ".mp3"))]

    if not archivos:
        print("⚠️ No hay archivos en 'mis_sonidos' — pon ahí tus sonidos primero")
        return False

    # Cargar sonidos si los encuentras
    bombo = cargar_sonido(os.path.join(CARPETA_SONIDOS, "bombo.wav")) if "bombo.wav" in archivos else None
    caja = cargar_sonido(os.path.join(CARPETA_SONIDOS, "caja.wav")) if "caja.wav" in archivos else None
    bajo = cargar_sonido(os.path.join(CARPETA_SONIDOS, "bajo.wav")) if "bajo.wav" in archivos else None

    # 🥁 Armar el ritmo
    for compas in range(int(duracion_seg / duracion_compas)):
        inicio = compas * muestras_compas

        # Agregar bombo en tiempo 1
        if bombo is not None:
            fin = min(inicio + len(bombo), total_muestras)
            beat[inicio:fin] += bombo[:fin-inicio] * 0.6

        # Agregar caja en tiempo 3
        if caja is not None:
            pos_caja = inicio + int(muestras_compas / 2)
            fin = min(pos_caja + len(caja), total_muestras)
            beat[pos_caja:fin] += caja[:fin-pos_caja] * 0.5

        # Agregar bajo continuo
        if bajo is not None:
            fin = min(inicio + len(bajo), total_muestras)
            beat[inicio:fin] += bajo[:fin-inicio] * 0.4

    # ✅ Si no tienes sonidos separados, usar el primer archivo como beat completo
    if np.max(np.abs(beat)) < 0.01:
        print("ℹ️ Usando tu archivo completo como beat...")
        beat_completo = cargar_sonido(os.path.join(CARPETA_SONIDOS, archivos[0]), duracion_seg)
        if beat_completo is not None:
            beat = beat_completo[:total_muestras]

    # 🎚️ Control final para que NO sature
    beat = np.clip(beat, -0.7, 0.7)
    beat = beat * 0.8

    # Guardar
    wavfile.write(ruta_salida, sr, (beat * 32767).astype(np.int16))
    audio_final = AudioSegment.from_wav(ruta_salida)
    audio_final = effects.normalize(audio_final, headroom=-3.0)
    audio_final.export(ruta_salida, format="wav", bitrate="192k")

    print(f"✅ Beat generado con tus sonidos: {ruta_salida}")
    return True

# ---------------- PRUEBA ----------------
if __name__ == "__main__":
    print("🎹 Generando beat usando tus propios sonidos...")
    generar_beat_con_tus_sonidos()
    print("🏁 Listo")
