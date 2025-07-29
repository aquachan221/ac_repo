import psutil
from datetime import datetime
import time
import socket
import requests

previous_connections = set()

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

while True:
    current_connections = set()

    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
            current_connections.add((conn.pid, conn.laddr, conn.raddr))

    new_conns = current_connections - previous_connections
    closed_conns = previous_connections - current_connections

    if new_conns or closed_conns:
        with open("newo_aqc.txt", "a", encoding="utf-8") as log_file:
            timestamp = datetime.now().isoformat()
            log_file.write(f"\n--- Network Change at {timestamp} ---\n")

            for conn in new_conns:
                pid, laddr, raddr = conn
                try:
                    pname = psutil.Process(pid).name()
                except Exception:
                    pname = "N/A"
                rhost = resolve_hostname(raddr.ip)
                geo = get_geolocation(raddr.ip)
                log_file.write(f"[START] {pname} (PID: {pid}) {laddr.ip}:{laddr.port} -> {raddr.ip}:{raddr.port} ({rhost}) [{geo}]\n")

            for conn in closed_conns:
                pid, laddr, raddr = conn
                try:
                    pname = psutil.Process(pid).name()
                except Exception:
                    pname = "N/A"
                rhost = resolve_hostname(raddr.ip)
                geo = get_geolocation(raddr.ip)
                log_file.write(f"[END]   {pname} (PID: {pid}) {laddr.ip}:{laddr.port} -> {raddr.ip}:{raddr.port} ({rhost}) [{geo}]\n")

    previous_connections = current_connections
    time.sleep(5)
