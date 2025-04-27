import speech_recognition as sr

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Escuchando tu voz... (habla ahora)")
        recognizer.adjust_for_ambient_noise(source)  # Calibrar ruido ambiente

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio, language="es-ES")
            print(f"🔎 Capturado: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("⌛ Tiempo de espera agotado, no se detectó voz.")
            return None
        except sr.UnknownValueError:
            print("❓ No se pudo entender el audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Error con el servicio de reconocimiento de voz: {e}")
            return None
