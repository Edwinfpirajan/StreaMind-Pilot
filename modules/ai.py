import requests
import pyttsx3
from modules.config import load_config

config = load_config()

# Configurar pyttsx3 para hablar
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

def interpret_command(text):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": config["model_name"],  # 👈 Aquí leemos desde config.json
        "prompt": f"Actúa como un asistente de streaming llamado Nova. El usuario dijo: '{text}'. ¿Qué intención detectas? Responde SOLO en una palabra: save_replay, start_recording, stop_recording, change_scene, ban_user, mute_chat, saludo",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        ia_response = data.get("response", "").strip().lower()
        print(f"🤖 IA interpretó como intención: {ia_response}")

        if ia_response == "saludo":
            hablar("Hola, soy Nova. Lista para ayudarte en tu stream.")
        elif ia_response == "save_replay":
            hablar("Guardando el último clip.")
        elif ia_response == "start_recording":
            hablar("Iniciando grabación.")
        elif ia_response == "stop_recording":
            hablar("Deteniendo grabación.")
        elif ia_response == "change_scene":
            hablar("Cambiando de escena.")
        elif ia_response == "ban_user":
            hablar("Procediendo a banear al usuario.")
        elif ia_response == "mute_chat":
            hablar("Silenciando el chat.")
        else:
            hablar("No entendí el comando, ¿puedes repetirlo?")

        return ia_response

    except Exception as e:
        print(f"❌ Error al conectar con OLLAMA: {e}")
        hablar("Hubo un error conectando a mi cerebro.")
        return None
