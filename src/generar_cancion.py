from .utils import asegurar_carpeta
from .tts_engine import MotorTTS
from .rhythm_sync import SincronizadorRitmo
from .voice_convert import ConvertidorVoz
from .audio_merge import unir_voz_y_beat, convertir_a_mp3

def generar_cancion(texto, ruta_beat, carpeta_salida="../assets/salidas", bpm=133):
    asegurar_carpeta(carpeta_salida)

    # Rutas temporales
    voz_base = f"{carpeta_salida}/voz_base.wav"
    voz_ajustada = f"{carpeta_salida}/voz_ajustada.wav"
    voz_rap = f"{carpeta_salida}/voz_rap.wav"
    final_wav = f"{carpeta_salida}/cancion_final.wav"
    final_mp3 = f"{carpeta_salida}/cancion_final.mp3"

    # Flujo completo
    tts = MotorTTS()
    tts.generar_voz(texto, voz_base)

    sincro = SincronizadorRitmo(bpm_objetivo=bpm)
    sincro.ajustar_a_bpm(voz_base, voz_ajustada)

    convertidor = ConvertidorVoz()
    convertidor.aplicar_estilo_rap(voz_ajustada, voz_rap)

    unir_voz_y_beat(voz_rap, ruta_beat, final_wav)
    convertir_a_mp3(final_wav, final_mp3)

    print("🎉 ¡Proceso finalizado con éxito!")
    return final_mp3

# Ejemplo de prueba
if __name__ == "__main__":
    letra_ejemplo = """Bienvenidos a la cancha leyendas!
Solo uno se alzará con la victoria eh eh.

Sin egoísmo no puedo avanzar
tu mentalidad es mediocre y nada más
mejor ni pienses en entrar
si no tienes ganas de luchar
"""
    generar_cancion(letra_ejemplo, ruta_beat="../assets/beats/beat_133bpm.wav")
