from modules.config import load_config
import requests
from modules.speak import speak

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

# 🧠 Función para hablar después de ejecutar algo
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

# ✨ Pedir a Ollama interpretación directa de comandos
def ask_ollama(prompt):
    model = config.get('model', 'phi3')
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": f"""
Eres un asistente de control de OBS Studio.
Tu única función es responder únicamente uno de estos comandos EXACTOS:
- start_recording
- stop_recording
- start_streaming
- stop_streaming
- save_replay

No respondas frases ni explicaciones.
Si no puedes interpretar el comando, responde exactamente: none

El usuario dice: "{prompt}"
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

# ✨ Interpretar y responder
def interpret_command(text):
    """Interpreta texto y ejecuta acción + respuesta hablada."""
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
