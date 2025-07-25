import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message):
    disconnected = []
    for client in clients:
        try:
            client.send(message)
        except:
            disconnected.append(client)
    for client in disconnected:
        if client in clients:
            clients.remove(client)
            try:
                client.close()
            except:
                pass

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            clients.remove(client)
            client.close()
            break


# ANSI color codes for dark mode terminal output
class Colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def print_dark(text, color=Colors.OKBLUE):
    print(f"{color}{text}{Colors.ENDC}")

print_dark("the running is the run the run the run the sevafer", Colors.OKGREEN)
while True:
    client, addr = server.accept()
    print_dark(f"Connected to {addr}", Colors.OKBLUE)
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()