import os
import socket
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_local_subnet():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = ipaddress.ip_network(local_ip + '/24', strict=False)
        return subnet
    except Exception as e:
        print(f"[!] Failed to detect local subnet: {e}")
        return ipaddress.ip_network('192.168.1.0/24', strict=False)

def get_arp_devices():
    devices = []
    try:
        output = subprocess.check_output("arp -a", shell=True).decode()
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0].strip("()")
                try:
                    ipaddress.ip_address(ip)
                    devices.append(ip)
                except ValueError:
                    continue
    except Exception as e:
        print(f"[!] Failed to read ARP cache: {e}")
    return devices

def is_reachable(ip):
    command = ['ping', '-n', '1', '-w', '300', str(ip)] if os.name == 'nt' else ['ping', '-c', '1', '-W', '1', str(ip)]
    try:
        return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except Exception:
        return False

def resolve_name(ip):
    if not is_reachable(ip):
        return str(ip), None
    try:
        host = socket.gethostbyaddr(str(ip))
        return str(ip), host[0]
    except (socket.herror, Exception):
        return str(ip), None

clear()

active_devices = []
named_devices = []

network = get_local_subnet()
print(f"[+] Detected subnet: {network}\n")

arp_known = get_arp_devices()

arp_in_subnet = [ip for ip in arp_known if ipaddress.ip_address(ip) in network]

with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(resolve_name, arp_in_subnet)
    for ip, hostname in results:
        print(f"[🔍] {ip}" + (f" ➜ {hostname}" if hostname else " ➜ (no name)"))
        active_devices.append(ip)
        if hostname:
            named_devices.append((ip, hostname))

print(f"\nTotal responding ARP-known devices: {len(active_devices)}")
print(f"Named devices: {len(named_devices)}\n")

for ip, name in named_devices:
    print(f" - {ip}: {name}")