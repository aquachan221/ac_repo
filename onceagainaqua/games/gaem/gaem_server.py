import socket
import threading
import pickle

HOST = '0.0.0.0'
PORT = 5555


import random
snakes = {}  # client_id -> list of segments [[x, y], ...]
client_id = 0
lock = threading.Lock()
food = []  # list of [x, y]
FOOD_COUNT = 20
# Infinite map: allow fruit anywhere in a large range (simulate infinite)
COORD_RANGE = 1000000  # +/-1,000,000

def handle_client(conn, addr, cid):
    global snakes, food
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            # Expecting: {'snake': [[x, y], ...]}
            msg = pickle.loads(data)
            with lock:
                snakes[cid] = msg['snake']
                # Check for food eaten
                head = snakes[cid][0]
                for f in food[:]:
                    if (abs(head[0] - f[0]) < 15) and (abs(head[1] - f[1]) < 15):
                        food.remove(f)
                        # Grow snake by duplicating last segment
                        snakes[cid].append(snakes[cid][-1][:])
                        break
                # Replenish food anywhere in infinite map
                while len(food) < FOOD_COUNT:
                    food.append([
                        random.randint(-COORD_RANGE, COORD_RANGE),
                        random.randint(-COORD_RANGE, COORD_RANGE)
                    ])
                update = pickle.dumps({'snakes': snakes, 'food': food})
            conn.sendall(update)
    except:
        pass
    finally:
        with lock:
            if cid in snakes:
                del snakes[cid]
        conn.close()

def start_server():
    global client_id, food
    # Only initialize food if empty (prevents duplicate food on server restart)
    if not food:
        for _ in range(FOOD_COUNT):
            food.append([
                random.randint(-COORD_RANGE, COORD_RANGE),
                random.randint(-COORD_RANGE, COORD_RANGE)
            ])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        cid = client_id
        client_id += 1
        # Start each snake with 5 segments at random position in infinite map
        start_x = random.randint(-COORD_RANGE, COORD_RANGE)
        start_y = random.randint(-COORD_RANGE, COORD_RANGE)
        snake = [[start_x, start_y]]
        for i in range(1, 5):
            snake.append([start_x - i*10, start_y])
        with lock:
            snakes[cid] = snake
        threading.Thread(target=handle_client, args=(conn, addr, cid), daemon=True).start()

start_server()