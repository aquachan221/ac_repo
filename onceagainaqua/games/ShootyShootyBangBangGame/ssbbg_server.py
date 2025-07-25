import socket
import threading
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="Unnamed Server")
parser.add_argument("--max", type=int, default=2)
parser.add_argument("--password", default="")
args = parser.parse_args()

HOST = "0.0.0.0"
TCP_PORT = 5555
UDP_PORT = 54545
MAX_PLAYERS = args.max
BASE_POS = [(100 + i * 150, 300) for i in range(MAX_PLAYERS)]

players = [{} for _ in range(MAX_PLAYERS)]
lock = threading.Lock()

def broadcast_listener():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("", UDP_PORT))
    while True:
        try:
            data, addr = udp.recvfrom(1024)
            if data.decode() == "DISCOVER_SSBBG":
                with lock:
                    count = sum(1 for p in players if p)
                msg = f"{args.name}|{count}/{MAX_PLAYERS}|{socket.gethostbyname(socket.gethostname())}"
                udp.sendto(msg.encode(), addr)
        except:
            continue

def detect_hits():
    for i in range(MAX_PLAYERS):
        target = players[i]
        if not target.get("alive", True): continue
        tx, ty = target.get("x", 0), target.get("y", 0)
        for j in range(MAX_PLAYERS):
            if i == j: continue
            shooter = players[j]
            for b in shooter.get("bullets", []):
                bx, by = b[0], b[1]
                if (bx - tx)**2 + (by - ty)**2 < 400:
                    target["x"], target["y"] = BASE_POS[i]
                    target["alive"] = True
                    shooter["score"] = shooter.get("score", 0) + 1
                    shooter["bullets"].remove(b)
                    return

def handle_client(conn, pid):
    conn.send(pickle.dumps({"id": pid, "base": BASE_POS[pid]}))
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            with lock:
                players[pid] = data
                detect_hits()
            conn.send(pickle.dumps(players))
        except:
            break
    print(f"[Player {pid}] disconnected")
    conn.close()

def main():
    print(f"[🔊] Hosting '{args.name}' with max {MAX_PLAYERS} players")
    if args.password:
        print("[🔐] Password enabled")

    threading.Thread(target=broadcast_listener, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen()

    pid = 0
    while pid < MAX_PLAYERS:
        conn, addr = server.accept()
        print(f"[+] Player {pid} connected from {addr}")
        threading.Thread(target=handle_client, args=(conn, pid)).start()
        pid += 1

if __name__ == "__main__":
    main()