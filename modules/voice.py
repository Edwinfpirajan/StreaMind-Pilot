import speech_recognition as sr
from modules.config import load_config

config = load_config()

def listen_for_command():
    """Capture voice input and process it based on the wake word."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(f"🎙️ Listening... (Language: {config['language']}, Wake word: '{config['wake_word']}')")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=25)
            command = recognizer.recognize_google(audio, language=config['language'])
            command = command.lower()
            print(f"🔎 Captured: {command}")

            if config['wake_word'] in command:
                cleaned_command = command.replace(config['wake_word'], '', 1).strip()
                return cleaned_command
            else:
                print("🙈 Wake word not detected.")
                return None

        except sr.WaitTimeoutError:
            print("⌛ Timeout reached, no voice detected.")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Voice recognition service error: {e}")
            return None
