# modules/conversation.py

from modules.voice import listen_for_command
from modules.speak import speak
from modules.ai import chat_with_ollama

def conversation_mode():
    """Modo conversación real con Ana usando Ollama."""
    speak("No entendí tu orden. ¿Quieres conversar un momento? Puedes decir 'ok Ana' para finalizar.")

    while True:
        command_text = listen_for_command()
        if not command_text:
            continue

        command_text = command_text.lower().strip()

        # ✅ Detectar si quieres finalizar la conversación
        if any(phrase in command_text for phrase in ["ok ana", "gracias ana", "finalizar ana", "listo ana"]):
            speak("Perfecto, volvamos a las órdenes principales.")
            break

        # ✨ Pedimos respuesta real a Ollama
        response = chat_with_ollama(command_text)
        if response:
            speak(response)
        else:
            speak("Estoy aquí para escucharte.")
