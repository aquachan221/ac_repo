import socket, threading, pickle, random, time

HOST = '0.0.0.0'
PORT = 5555


players = {}     # {id: {"pos": [x, y], "alive": True, "input": ...}}
bots = []        # [{"pos": [x, y], "alive": True, "cooldown": int}]
map_data = []    # list of obstacle rects
weapons = []     # [{"x": int, "y": int, "type": str}]
bullets = []     # [{"pos": [x, y], "dir": [dx, dy], "owner": str}]
MAP_RADIUS = 800
MAP_CENTER = (1000, 1000)
flood_level = MAP_CENTER[1] + MAP_RADIUS  # Start flood below map
lock = threading.Lock()

def generate_map():
    global map_data, weapons
    map_data = []
    weapons = []

    # Place obstacles only inside the circle
    for _ in range(60):
        while True:
            x = random.randint(MAP_CENTER[0] - MAP_RADIUS + 40, MAP_CENTER[0] + MAP_RADIUS - 40)
            y = random.randint(MAP_CENTER[1] - MAP_RADIUS + 40, MAP_CENTER[1] + MAP_RADIUS - 40)
            if (x - MAP_CENTER[0]) ** 2 + (y - MAP_CENTER[1]) ** 2 < (MAP_RADIUS - 40) ** 2:
                break
        w = random.randint(20, 60)
        h = random.randint(20, 60)
        map_data.append([x, y, w, h])

    for _ in range(20):
        while True:
            wx = random.randint(MAP_CENTER[0] - MAP_RADIUS + 40, MAP_CENTER[0] + MAP_RADIUS - 40)
            wy = random.randint(MAP_CENTER[1] - MAP_RADIUS + 40, MAP_CENTER[1] + MAP_RADIUS - 40)
            if (wx - MAP_CENTER[0]) ** 2 + (wy - MAP_CENTER[1]) ** 2 < (MAP_RADIUS - 40) ** 2:
                break
        weapons.append({"x": wx, "y": wy, "type": random.choice(["pistol", "rifle", "launcher"])})

def update_flood():
    global flood_level
    flood_level = max(0, flood_level - 0.2)

def run_bots():
    # Bots are disabled: no movement, no bullets
    while True:
        time.sleep(0.5)
        pass

def update_bullets():
    global bullets
    new_bullets = []
    for bullet in bullets:
        bullet["pos"][0] += bullet["dir"][0] * 5
        bullet["pos"][1] += bullet["dir"][1] * 5
        bx, by = bullet["pos"]

        for cid, p in players.items():
            if p["alive"]:
                px, py = p["pos"]
                if abs(px - bx) < 10 and abs(py - by) < 10:
                    p["alive"] = False
                    break
        else:
            new_bullets.append(bullet)
    bullets = new_bullets

def handle_client(conn, cid):
    global players
    try:
        while True:
            data = conn.recv(1024)
            if not data: break
            input_cmd = pickle.loads(data)
            with lock:
                players[cid]["input"] = input_cmd

                # Apply movement
                if players[cid]["alive"]:
                    move = input_cmd.get("move", [0, 0])

                    # Try to move, but check collision with boxes
                    px, py = players[cid]["pos"]
                    size = 20  # player size
                    new_x = px + move[0] * 3
                    new_y = py + move[1] * 3
                    # Check circle boundary
                    dx = new_x - MAP_CENTER[0]
                    dy = new_y - MAP_CENTER[1]
                    if dx * dx + dy * dy >= MAP_RADIUS * MAP_RADIUS:
                        new_x, new_y = px, py

                    # Check collision with boxes (AABB)
                    def collides(nx, ny):
                        for ox, oy, ow, oh in map_data:
                            if nx + size > ox and nx < ox + ow and ny + size > oy and ny < oy + oh:
                                return True
                        return False

                    # Try x move only
                    if not collides(new_x, py):
                        px = new_x
                    # Try y move only
                    if not collides(px, new_y):
                        py = new_y
                    # Try both (if neither blocked)
                    if not collides(new_x, new_y):
                        px, py = new_x, new_y

                    players[cid]["pos"] = [px, py]

                    # Flood check (if below flood)
                    if players[cid]["pos"][1] > flood_level:
                        players[cid]["alive"] = False

                update_flood()
                update_bullets()

                payload = {
                    "players": players,
                    "bots": bots,
                    "map": map_data,
                    "weapons": weapons,
                    "flood": flood_level,
                    "bullets": bullets
                }
            conn.sendall(pickle.dumps(payload))
    except:
        pass
    with lock:
        del players[cid]
    conn.close()

def start():
    global bots, players, bullets, flood_level
    while True:
        generate_map()
        bots = []
        players = {}
        bullets = []
        flood_level = MAP_CENTER[1] + MAP_RADIUS
        for i in range(8):
            # Place bots randomly in circle
            while True:
                bx = random.randint(MAP_CENTER[0] - MAP_RADIUS + 40, MAP_CENTER[0] + MAP_RADIUS - 40)
                by = random.randint(MAP_CENTER[1] - MAP_RADIUS + 40, MAP_CENTER[1] + MAP_RADIUS - 40)
                if (bx - MAP_CENTER[0]) ** 2 + (by - MAP_CENTER[1]) ** 2 < (MAP_RADIUS - 40) ** 2:
                    break
            bots.append({"pos": [bx, by], "alive": True, "cooldown": 0})
        threading.Thread(target=run_bots, daemon=True).start()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print("[SERVER STARTED]")

        cid = 0
        client_threads = []
        def all_dead():
            return all(not p["alive"] for p in players.values()) if players else False

        while True:
            # Check for all players dead
            if all_dead():
                print("All players dead! Restarting in 5 seconds...")
                for t in range(5, 0, -1):
                    print(f"Restarting in {t}...")
                    time.sleep(1)
                break
            server.settimeout(0.5)
            try:
                conn, _ = server.accept()
            except socket.timeout:
                continue
            with lock:
                # Place player randomly in circle
                while True:
                    px = random.randint(MAP_CENTER[0] - MAP_RADIUS + 40, MAP_CENTER[0] + MAP_RADIUS - 40)
                    py = random.randint(MAP_CENTER[1] - MAP_RADIUS + 40, MAP_CENTER[1] + MAP_RADIUS - 40)
                    if (px - MAP_CENTER[0]) ** 2 + (py - MAP_CENTER[1]) ** 2 < (MAP_RADIUS - 40) ** 2:
                        break
                players[cid] = {"pos": [px, py], "alive": True, "input": None}
            th = threading.Thread(target=handle_client, args=(conn, cid), daemon=True)
            th.start()
            client_threads.append(th)
            cid += 1

start()