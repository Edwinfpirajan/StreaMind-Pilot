from modules.voice import listen_for_command
from modules.ai import interpret_command
from modules.obs_control import execute_action
from modules.conversation import conversation_mode
from modules.config import load_config

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
            else:
                conversation_mode()

if __name__ == "__main__":
    main()
