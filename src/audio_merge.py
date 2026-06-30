import numpy as np
from .utils import cargar_audio, guardar_audio

def normalizar_volumen(señal, nivel=0.8):
    max_amp = np.max(np.abs(señal))
    if max_amp == 0:
        return señal
    return señal * (nivel / max_amp)

def unir_voz_y_beat(ruta_voz, ruta_beat, ruta_salida, vol_voz=1.0, vol_beat=0.7):
    voz, sr = cargar_audio(ruta_voz)
    beat, _ = cargar_audio(ruta_beat, sr=sr)

    min_longitud = min(len(voz), len(beat))
    voz = voz[:min_longitud] * vol_voz
    beat = beat[:min_longitud] * vol_beat

    mezcla = normalizar_volumen(voz + beat)
    guardar_audio(mezcla, ruta_salida, sr)
    print(f"✅ Mezcla final lista: {ruta_salida}")
    return ruta_salida
