import json
import os

def load_config():
    """Load configuration settings from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return {
            "obs_host": "localhost",
            "obs_port": 4455,
            "obs_password": "jarvisjunior",
            "language": "es-ES",
            "wake_word": "nova",
            "model_name": "phi3"
        }
