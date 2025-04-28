# modules/ai.py

from modules.config import load_config
from modules.speak import speak
import requests

# Configuración cargada
config = load_config()

# Lista de comandos válidos
ALLOWED_COMMANDS = [
    "start_recording",
    "stop_recording",
    "start_streaming",
    "stop_streaming",
    "save_replay"
]

# 🧠 Función para hablar después de ejecutar una acción
def respond_after_action(command):
    responses = {
        "start_recording": "¡Grabación iniciada!",
        "stop_recording": "Grabación detenida.",
        "start_streaming": "¡Estamos en vivo!",
        "stop_streaming": "Transmisión finalizada.",
        "save_replay": "Clip guardado exitosamente."
    }
    response = responses.get(command, "Acción completada.")
    print(f"🗣️ {response}")
    speak(response)

# ✨ Pedir interpretación a Ollama
def ask_ollama(prompt):
    model = config.get('model', 'phi3')
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": f"""
Eres un asistente de control de OBS Studio.
Solo debes responder UNO de estos comandos exactos:
- start_recording (cuando digan grabar, iniciar grabación, comenzar grabación)
- stop_recording (cuando digan detener grabación, parar grabación)
- start_streaming (cuando digan transmitir, iniciar en vivo, empezar en vivo)
- stop_streaming (cuando digan detener transmisión, parar transmisión)
- save_replay (cuando digan haz un clip, guardar clip, hace un clip, guardar repetición)

Si el mensaje del usuario no corresponde, responde solo: none

Usuario dice: "{prompt}"
""",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        intent = data.get("response", "").strip().lower()
        print(f"🧠 IA Respondió: {intent}")
        return intent
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return "none"

# ✨ Interpretar y validar
def interpret_command(text):
    command = ask_ollama(text)

    if command in ALLOWED_COMMANDS:
        return command
    elif command == "none":
        print("⚠️ IA no pudo interpretar un comando válido.")
        speak("No entendí tu orden. ¿Podrías repetirla?")
        return None
    else:
        print(f"⚠️ Comando recibido no permitido: {command}")
        speak("Orden no reconocida.")
        return None
