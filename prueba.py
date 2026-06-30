import os
import numpy as np
import soundfile as sf
from gtts import gTTS
from pydub import AudioSegment
import librosa
import librosa.effects

# Ruta FFmpeg
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

CARPETA_SALIDAS = os.path.join("assets", "salidas")
os.makedirs(CARPETA_SALIDAS, exist_ok=True)

RUTA_MP3_VOZ = r"C:\Users\USER\Documents\IA-cover-music-main\mi_voz_limpia.mp3.mp3"

def extraer_perfil_voz(ruta_referencia):
    y, sr = librosa.load(ruta_referencia, sr=16000, duration=25)
    centroide = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    return {"centroide": centroide, "sr": sr}

def aplicar_timbre(ruta_audio, perfil):
    y, sr = librosa.load(ruta_audio, sr=perfil["sr"])
    centroide_y = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    if centroide_y > 80 and perfil["centroide"] > 80:
        pasos = np.log2(perfil["centroide"] / centroide_y) * 12
        pasos = np.clip(pasos, -3, 3)
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pasos)
    sf.write(ruta_audio, y, sr)
    return ruta_audio

def ajustar_ritmo(ruta_audio, bpm):
    y, sr = librosa.load(ruta_audio, sr=16000)
    duracion = len(y) / sr
    factor = duracion / (duracion * 120 / bpm)
    factor = np.clip(factor, 0.82, 1.18)
    y = librosa.effects.time_stretch(y, rate=factor)
    sf.write(ruta_audio, y, sr)
    return ruta_audio

def texto_a_canto(texto: str, bpm: int = 120):
    if not os.path.exists(RUTA_MP3_VOZ):
        raise FileNotFoundError(f"No encontrado: {RUTA_MP3_VOZ}")
    perfil = extraer_perfil_voz(RUTA_MP3_VOZ)
    frases = [f.strip() for f in texto.replace("\n", " ").split(".") if len(f.strip()) > 2]
    audio_total = AudioSegment.silent(duration=0)
    for i, frase in enumerate(frases):
        ruta_temp = os.path.join(CARPETA_SALIDAS, f"temp_{i}.mp3")
        gTTS(text=frase, lang="es", slow=False).save(ruta_temp)
        audio = AudioSegment.from_mp3(ruta_temp)
        ruta_wav = ruta_temp.replace(".mp3", ".wav")
        audio.export(ruta_wav, format="wav")
        aplicar_timbre(ruta_wav, perfil)
        ajustar_ritmo(ruta_wav, bpm)
        y, sr = librosa.load(ruta_wav, sr=16000)
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=(i % 5) - 2)
        sf.write(ruta_wav, y, sr)
        audio_total += AudioSegment.from_wav(ruta_wav) + AudioSegment.silent(duration=int(60000 / bpm * 0.35))
    ruta_final = os.path.join(CARPETA_SALIDAS, "voz_cantada.wav")
    audio_total.export(ruta_final, format="wav")
    return ruta_final

# Prueba rápida
if __name__ == "__main__":
    print("✅ Iniciando prueba...")
    letra = "Hola, esta es una prueba para ver si funciona la voz con tu timbre."
    salida = texto_a_canto(letra, bpm=100)
    print(f"✅ Archivo generado en: {salida}")
