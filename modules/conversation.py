# modules/conversation.py

from modules.voice import listen_for_command
from modules.speak import speak

def conversation_mode():
    """Modo conversación amigable con Ana cuando no entiende un comando."""
    speak("No entendí tu orden. ¿Quieres conversar un momento? Puedes decir 'ok Ana' para finalizar.")

    while True:
        command_text = listen_for_command()
        if not command_text:
            continue

        command_text = command_text.lower()

        if "ok ana" in command_text or "gracias ana" in command_text or "listo ana" in command_text:
            speak("Perfecto, volvamos a las órdenes principales.")
            break
        else:
            responses = [
                "Claro, te escucho.",
                "Cuéntame más.",
                "¿Qué más quieres decirme?",
                "Estoy aquí para ayudarte.",
                "Te sigo escuchando."
            ]
            import random
            speak(random.choice(responses))
