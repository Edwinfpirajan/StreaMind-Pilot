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
    """Envía un mensaje a la instancia local de Ollama con un contexto específico para streaming."""
    model = config.get('model_name', 'phi3')
    url = "http://localhost:11434/api/generate"
    
    system_instruction = (
        "Eres una asistente de streaming. Tu trabajo es interpretar comandos de voz que controlan OBS Studio. "
        "Reconoces intenciones como: iniciar grabación, guardar clip, detener grabación, cambiar de escena, mutear audio, banear usuarios, y dar saludos. "
        "Debes responder únicamente la intención como un verbo simple o frase corta (ej: 'iniciar grabación', 'guardar clip', 'detener grabación'). "
        "No des respuestas largas, no saludes, no expliques."
    )

    full_prompt = f"{system_instruction}\n\nUsuario dice: {prompt}\nRespuesta:"

    payload = {
        "model": model,
        "prompt": full_prompt,
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
    print(f"🔎 Command received: {text}")
    intent = ask_ollama(text)
    print(f"🔍 Interpreted intent: {intent}")

    if not intent:
        speak("No entendí, ¿puedes repetirlo?")
        return None

    intent = intent.lower()

    if "iniciar grabación" in intent or "empezar a grabar" in intent or "grabar" in intent:
        speak("Iniciando grabación.")
        return "start_recording"
    elif "guardar clip" in intent or "guardar replay" in intent or "guardar" in intent:
        speak("Guardando el último clip.")
        return "save_replay"
    elif "detener grabación" in intent or "parar grabación" in intent or "detener" in intent:
        speak("Deteniendo la grabación.")
        return "stop_recording"
    else:
        speak(intent)
        return None
