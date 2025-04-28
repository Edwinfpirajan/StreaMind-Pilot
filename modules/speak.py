import asyncio
import edge_tts
import tempfile
import os
from playsound import playsound

VOICE = "es-MX-DaliaNeural"
RATE = "+5%"

async def speak_async(text):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)

    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        temp_audio_path = tmpfile.name

    # Escribir el audio que llega del stream
    with open(temp_audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

    # Reproducir el archivo
    playsound(temp_audio_path)

    # Eliminar archivo temporal después de reproducir
    os.remove(temp_audio_path)

def speak(text):
    """Habla el texto usando una voz natural."""
    try:
        asyncio.run(speak_async(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_async(text))
