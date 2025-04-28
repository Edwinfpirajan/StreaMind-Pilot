import os
import time
import pygame
import pyttsx3
import requests
import speech_recognition as sr
from modules.config import load_config

# Cargar configuración
config = load_config()

# Inicializar el motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Ajusta la velocidad del habla (puedes cambiarla)
engine.setProperty('volume', 1)  # Ajusta el volumen (de 0.0 a 1.0)

def speak(text):
    """Genera y reproduce el habla usando pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Escucha el comando después de detectar el wake word."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Ajustamos el timeout y el límite de la frase
            command = recognizer.recognize_google(audio, language=config['language'])
            print(f"🔎 Command captured: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("⌛ Timeout reached, no voice detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with Google Speech Recognition service: {e}")
            return None

def ask_ollama(prompt):
    """Envía un mensaje a la instancia local de Ollama y obtiene la respuesta."""
    model = config.get('model', 'phi3')
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data.get("response", "").strip().lower()
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return ""

def interpret_command(text):
    """Interpreta el comando del usuario y decide la acción a tomar."""
    print(f"🔎 Command received: {text}")  # Log para verificar que el comando fue recibido correctamente
    intent = ask_ollama(text)
    print(f"🔍 Interpreted intent: {intent}")  # Log para verificar la interpretación del comando

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
        speak(intent)
        return None