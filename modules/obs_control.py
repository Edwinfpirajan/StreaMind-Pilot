from obswebsocket import obsws, requests

# Global WebSocket connection
ws = None

def connect_to_obs(config):
    """Establish a connection to OBS via WebSocket."""
    global ws
    try:
        ws = obsws(config['obs_host'], config['obs_port'], config['obs_password'])
        ws.connect()
        print("✅ Connected to OBS via WebSocket")
    except Exception as e:
        print(f"❌ Error connecting to OBS: {e}")

def execute_action(action, config):
    """Execute an action in OBS based on the interpreted AI intention."""
    global ws
    if not ws:
        connect_to_obs(config)

    try:
        if action == "save_replay":
            ws.call(requests.SaveReplayBuffer())
            print("🎬 Replay buffer saved successfully.")
        elif action == "start_recording":
            ws.call(requests.StartRecording())
            print("⏺️ Recording started.")
        elif action == "stop_recording":
            ws.call(requests.StopRecording())
            print("⏹️ Recording stopped.")
        else:
            print(f"⚠️ Unrecognized action: {action}")
    except Exception as e:
        print(f"❌ Error executing action '{action}': {e}")
