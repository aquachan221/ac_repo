import socket#type: ignore
import threading#type: ignore
import json

SERVER_IP = "0.0.0.0"
SERVER_PORT = 50000
BUFFER_SIZE = 1024

players = {}

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    players[addr] = {"x": 100, "y": 100}

    while True:
        try:
            data = conn.recv(BUFFER_SIZE).decode()

            if not data:  # Check if data is empty (client disconnected)
                print(f"Client {addr} disconnected.")
                break

            if data.startswith("MOVE"):
                direction = data.split()[1]
                if direction == "W":
                    players[addr]["y"] -= 5
                elif direction == "S":
                    players[addr]["y"] += 5
                elif direction == "A":
                    players[addr]["x"] -= 5
                elif direction == "D":
                    players[addr]["x"] += 5
            
            print(f"Sending positions: {players}")  # Debugging log
            
            # Ensure connection is still alive before sending data
            try:
                conn.send(json.dumps(players).encode())
            except socket.error as e:
                print(f"Error sending data to {addr}: {e}")
                break
        except:
            del players[addr]
            conn.close()
            break

    del players[addr]
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print("Server started!")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

start_server()