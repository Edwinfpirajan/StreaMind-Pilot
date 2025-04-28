from obsws_python import ReqClient

# Global OBS client
obs_client = None

def connect_to_obs(config):
    """Establish a connection to OBS via WebSocket."""
    global obs_client
    if obs_client is None:
        try:
            obs_client = ReqClient(
                host=config['obs_host'],
                port=config['obs_port'],
                password=config['obs_password']
            )
            print("✅ Connected to OBS via WebSocket (obsws-python)")
        except Exception as e:
            print(f"❌ Error connecting to OBS: {e}")

def is_recording():
    """Check if OBS is currently recording."""
    global obs_client
    try:
        status = obs_client.get_record_status()
        return status.output_active
    except Exception as e:
        print(f"❌ Error checking recording status: {e}")
        return False

def is_streaming():
    """Check if OBS is currently streaming."""
    global obs_client
    try:
        status = obs_client.get_stream_status()
        return status.output_active
    except Exception as e:
        print(f"❌ Error checking stream status: {e}")
        return False

def is_replay_buffer_active():
    """Check if the replay buffer is active."""
    global obs_client
    try:
        status = obs_client.get_replay_buffer_status()
        return status.output_active
    except Exception as e:
        print(f"❌ Error checking replay buffer status: {e}")
        return False

def start_replay_buffer_if_needed():
    """Start replay buffer if it's not already active."""
    if not is_replay_buffer_active():
        obs_client.start_replay_buffer()
        print("📼 Replay Buffer started.")

def stop_replay_buffer_if_needed():
    """Stop replay buffer if no recording or streaming is active."""
    if not is_recording() and not is_streaming():
        if is_replay_buffer_active():
            obs_client.stop_replay_buffer()
            print("🛑 Replay Buffer stopped.")

def execute_action(action, config):
    """Execute an action in OBS based on the interpreted AI intention."""
    global obs_client
    if obs_client is None:
        connect_to_obs(config)

    if obs_client is None:
        print("❌ No available connection to OBS.")
        return

    try:
        action = action.lower()
        print(f"➡️ Executing action in OBS: {action}")

        if action == "start_recording":
            if is_recording():
                print("⚠️ Already recording.")
            else:
                obs_client.start_record()
                print("⏺️ Recording started in OBS.")
            start_replay_buffer_if_needed()

        elif action == "start_streaming":
            if is_streaming():
                print("⚠️ Already streaming.")
            else:
                obs_client.start_stream()
                print("📡 Streaming started in OBS.")
            start_replay_buffer_if_needed()

        elif action == "stop_recording":
            if not is_recording():
                print("⚠️ No active recording to stop.")
            else:
                obs_client.stop_record()
                print("⏹️ Recording stopped in OBS.")
            stop_replay_buffer_if_needed()

        elif action == "stop_streaming":
            if not is_streaming():
                print("⚠️ No active stream to stop.")
            else:
                obs_client.stop_stream()
                print("🛑 Streaming stopped in OBS.")
            stop_replay_buffer_if_needed()

        elif action == "save_replay":
            obs_client.save_replay_buffer()
            print("🎬 Replay buffer saved.")

        else:
            print(f"⚠️ Action not recognized in OBS: {action}")

    except Exception as e:
        print(f"❌ Error executing action '{action}': {e}")
