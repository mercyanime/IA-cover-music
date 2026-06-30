import os
import librosa
import soundfile as sf
import ffmpeg
import numpy as np

def asegurar_carpeta(ruta):
    """Crea la carpeta si no existe"""
    if not os.path.exists(ruta):
        os.makedirs(ruta)

def cargar_audio(ruta, sr=44100):
    """Carga archivo de audio y devuelve señal + frecuencia de muestreo"""
    return librosa.load(ruta, sr=sr)

def guardar_audio(señal, ruta, sr=44100):
    """Guarda audio en formato WAV"""
    sf.write(ruta, señal, sr)

def cambiar_tono(señal, sr, semitonos):
    """Ajusta el tono sin alterar duración"""
    return librosa.effects.pitch_shift(y=señal, sr=sr, n_steps=semitonos)

def ajustar_velocidad(señal, factor):
    """Cambia velocidad manteniendo el tono"""
    return librosa.effects.time_stretch(y=señal, rate=factor)

def convertir_a_mp3(ruta_entrada, ruta_salida):
    """Convierte WAV a MP3 con FFmpeg"""
    try:
        ffmpeg.input(ruta_entrada).output(ruta_salida, format='mp3', audio_bitrate='192k').run(quiet=True, overwrite_output=True)
        return True
    except Exception as e:
        print(f"Error al convertir: {e}")
        return False
