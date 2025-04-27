from obswebsocket import obsws, requests

ws = None

def connect_to_obs(config):
    global ws
    try:
        ws = obsws(config['obs_host'], config['obs_port'], config['obs_password'])
        ws.connect()
        print("✅ Conectado a OBS vía WebSocket")
    except Exception as e:
        print(f"❌ Error conectando a OBS: {e}")

def execute_action(action, config):
    global ws
    if not ws:
        connect_to_obs(config)
    
    try:
        if action == "save_replay":
            ws.call(requests.SaveReplayBuffer())
            print("🎬 Clip guardado exitosamente en OBS.")
        elif action == "start_recording":
            ws.call(requests.StartRecording())
            print("⏺️ Grabación iniciada.")
        elif action == "stop_recording":
            ws.call(requests.StopRecording())
            print("⏹️ Grabación detenida.")
        else:
            print(f"⚠️ Acción no reconocida: {action}")
    except Exception as e:
        print(f"❌ Error ejecutando acción '{action}': {e}")
