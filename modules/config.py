import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return {
            "obs_host": "localhost",
            "obs_port": 4455,
            "obs_password": "tu_contraseña",
        }
