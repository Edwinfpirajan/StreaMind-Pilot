import os
import subprocess
import pygame
import requests
from modules.config import load_config

# Load configuration
config = load_config()

import os
import subprocess

import simpleaudio as sa

def speak(text):
    """Genera y reproduce el habla usando Piper (a través de piper.exe subprocess)."""
    piper_exe_path = os.path.join(os.getcwd(), "piper", "piper.exe")  # Ruta al ejecutable de Piper
    model_path = os.path.join(os.getcwd(), "models", "es_MX-ald-medium.onnx")  # Modelo correcto
    output_path = os.path.join(os.getcwd(), "output.wav")

    # Si el archivo de salida existe, lo eliminamos
    if os.path.exists(output_path):
        os.remove(output_path)

    # Comando para ejecutar Piper con el modelo y texto
    command = [
        piper_exe_path,
        "--model", model_path,
        "--output_file", output_path,
        "--text", text,
        "--length_scale", "1.1"  # Opcional, ajusta la velocidad del habla
    ]

    try:
        print("Running Piper...")
        # Ejecutamos Piper usando subprocess y capturamos la salida
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        print("Piper finished, output:")
        print(result.stdout)  # Muestra la salida estándar
        print(result.stderr)  # Muestra cualquier error

        # Verificamos si el archivo output.wav fue creado
        if os.path.exists(output_path):
            print(f"🎤 Archivo generado correctamente: {output_path}")
            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Espera hasta que termine de reproducir
                pygame.time.Clock().tick(10)
            print("🎶 Reproducción completada.")
        else:
            print("❌ Piper no generó output.wav.")
    except Exception as e:
        print(f"❌ Error al ejecutar Piper: {e}")


def ask_ollama(prompt):
    """Envía un prompt a la instancia local de Ollama y obtiene una respuesta."""
    model = config.get('model', 'phi3')
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        # Realiza la solicitud POST a Ollama
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip().lower()
    except Exception as e:
        print(f"❌ Error al conectar con Ollama: {e}")
        return ""

def interpret_command(text):
    """Interpreta el comando del usuario utilizando la respuesta de IA."""
    intent = ask_ollama(text)

    if not intent:
        speak("No entendí, ¿puedes repetirlo?")
        return None

    if "grabar" in intent:
        speak("Iniciando grabación.")
        return "start_recording"
    elif "clip" in intent or "guardar" in intent:
        speak("Guardando el último clip.")
        return "save_replay"
    elif "escena" in intent or "cambiar" in intent:
        speak("Cambiando de escena.")
        return "change_scene"
    elif "detener" in intent or "parar" in intent:
        speak("Deteniendo la grabación.")
        return "stop_recording"
    elif "mutear" in intent or "silenciar" in intent:
        speak("Silenciando el chat.")
        return "mute_chat"
    elif "banear" in intent or "expulsar" in intent:
        speak("Expulsando al usuario.")
        return "ban_user"
    elif "saludo" in intent or "saludar" in intent:
        speak(f"Hola, soy {config.get('wake_word', 'Nova')}. ¿Cómo puedo ayudarte hoy?")
        return "saludo"
    else:
        speak("No entendí el comando, ¿puedes repetirlo?")
        return None
