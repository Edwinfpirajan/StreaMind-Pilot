from modules.voice import listen_for_command
from modules.ai import interpret_command, respond_after_action
from modules.obs_control import execute_action
from modules.config import load_config
from modules.conversation import conversation_mode

def main():
    config = load_config()

    print(f"🎙️ StreamMind Pilot started. Listening for wake word: '{config['wake_word']}'...")

    while True:
        command_text = listen_for_command()
        if command_text:
            print(f"🔎 Command after wake word: {command_text}")
            action = interpret_command(command_text)

            if action:
                execute_action(action, config)
                respond_after_action(action)  # ✅ Después de ejecutar, ahora responde
            else:
                conversation_mode()

if __name__ == "__main__":
    main()
