import time
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
    global obs_client
    if not is_replay_buffer_active():
        try:
            obs_client.start_replay_buffer()
            print("📼 Replay Buffer started.")
        except Exception as e:
            print(f"❌ Error starting Replay Buffer: {e}")

def stop_replay_buffer_if_needed():
    """Stop replay buffer if no recording or streaming is active."""
    global obs_client
    time.sleep(1)  # Esperar un momento para que OBS actualice estado real
    if not is_recording() and not is_streaming():
        if is_replay_buffer_active():
            try:
                obs_client.stop_replay_buffer()
                print("🛑 Replay Buffer stopped because no recording or streaming are active.")
            except Exception as e:
                print(f"❌ Error stopping Replay Buffer: {e}")
        else:
            print("ℹ️ Replay Buffer was already stopped.")
    else:
        print("ℹ️ Replay Buffer remains active because recording or streaming is still ongoing.")

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
            try:
                obs_client.stop_record()
                print("⏹️ Recording stop requested to OBS.")
            except Exception as e:
                print(f"❌ Error stopping recording: {e}")

            time.sleep(1)

            if not is_recording():
                print("✅ Recording successfully stopped.")
            else:
                print("⚠️ Warning: Recording still appears active.")

            stop_replay_buffer_if_needed()

        elif action == "stop_streaming":
            try:
                obs_client.stop_stream()
                print("🛑 Streaming stop requested to OBS.")
            except Exception as e:
                print(f"❌ Error stopping streaming: {e}")

            time.sleep(1)

            if not is_streaming():
                print("✅ Streaming successfully stopped.")
            else:
                print("⚠️ Warning: Streaming still appears active.")

            stop_replay_buffer_if_needed()

        elif action == "save_replay":
            try:
                obs_client.save_replay_buffer()
                print("🎬 Replay buffer saved.")
            except Exception as e:
                print(f"❌ Error saving replay buffer: {e}")

        else:
            print(f"⚠️ Action not recognized in OBS: {action}")

    except Exception as e:
        print(f"❌ Error executing action '{action}': {e}")
