from modules.voice import listen_for_command
from modules.ai import interpret_command
from modules.obs_control import execute_action
from modules.config import load_config

def main():
    config = load_config()

    print(f"🎙️ StreamMind Pilot iniciado. Escuchando activación: '{config['wake_word']}'...")

    while True:
        command_text = listen_for_command()
        if command_text:
            print(f"🔎 Comando después del wake word: {command_text}")
            action = interpret_command(command_text)
            if action:
                execute_action(action, config)

if __name__ == "__main__":
    main()
