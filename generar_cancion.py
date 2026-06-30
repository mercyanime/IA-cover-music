import os
from gtts import gTTS
import librosa
import soundfile as sf
from pydub import AudioSegment

# Rutas automáticas
CARPETA_SALIDAS = os.path.join("activos", "salidas")
os.makedirs(CARPETA_SALIDAS, exist_ok=True)

def generar_cancion(texto_letra, ruta_ritmo, bpm):
    # 1. Generar voz desde texto
    ruta_voz_mp3 = os.path.join(CARPETA_SALIDAS, "voz_generada.mp3")
    ruta_voz_wav = os.path.join(CARPETA_SALIDAS, "voz_generada.wav")
    
    tts = gTTS(text=texto_letra, lang="es", slow=False)
    tts.save(ruta_voz_mp3)
    
    # Convertir a WAV para mezclar
    voz = AudioSegment.from_mp3(ruta_voz_mp3)
    voz.export(ruta_voz_wav, format="wav")

    # 2. Si hay ritmo, mezclamos
    ruta_final = os.path.join(CARPETA_SALIDAS, "cancion_final.wav")
    if os.path.exists(ruta_ritmo):
        try:
            beat = AudioSegment.from_file(ruta_ritmo)
            # Ajustar volumen
            voz = voz + 3
            beat = beat - 8
            # Mezclar
            mezcla = voz.overlay(beat, position=0)
            mezcla.export(ruta_final, format="wav")
        except:
            ruta_final = ruta_voz_wav
    else:
        ruta_final = ruta_voz_wav

    return ruta_final

if __name__ == "__main__":
    print("✅ Módulo listo con gTTS")
