import os
import socket
from concurrent.futures import ThreadPoolExecutor

target_host = '192.168.1.254'
port_range = range(1, 65535)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.5)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
    except Exception:
        pass

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, port_range)
