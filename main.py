from modules.voice import listen_for_command
from modules.ai import interpret_command
from modules.obs_control import execute_action
from modules.config import load_config

def main():
    config = load_config()

    print("🎙️ StreamMind Pilot iniciado. Escuchando comandos...")

    while True:
        command_text = listen_for_command()
        if command_text:
            print(f"🔎 Comando escuchado: {command_text}")
            action = interpret_command(command_text)
            if action:
                execute_action(action, config)

if __name__ == "__main__":
    main()
