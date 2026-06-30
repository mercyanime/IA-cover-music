# Interfaz sencilla para usar el generador
import gradio as gr
from src.generar_cancion import generar_cancion

def crear(texto, ruta_ritmo, bpm):
    return generar_cancion(texto, ruta_ritmo, int(bpm))

with gr.Blocks(title="Generador de Voz IA") as app:
    gr.Markdown("# 🎤 Generador de Rap / Canciones")
    texto = gr.Textbox(label="Tu letra", lines=8)
    bpm = gr.Number(label="BPM", value=133)
    ritmo = gr.Textbox(label="Ruta del archivo de ritmo")
    resultado = gr.File(label="Canción final")
    gr.Button("Generar").click(crear, [texto, ritmo, bpm], resultado)

if __name__ == "__main__":
    app.launch()
