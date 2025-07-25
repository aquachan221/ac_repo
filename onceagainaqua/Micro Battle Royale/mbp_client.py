import pygame, socket, pickle

HOST = 'Jojopooter'  # Replace with your server's IP
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MicroBattle Royale")
clock = pygame.time.Clock()

def send_input(keys):
    move = [0, 0]
    if keys[pygame.K_w]: move[1] -= 1
    if keys[pygame.K_s]: move[1] += 1
    if keys[pygame.K_a]: move[0] -= 1
    if keys[pygame.K_d]: move[0] += 1
    sock.sendall(pickle.dumps({"move": move}))


font = pygame.font.SysFont(None, 28)
alive_last = True
death_timer = 0


# Map constants (must match server)
MAP_RADIUS = 800
MAP_CENTER = (1000, 1000)

def get_player_pos(state):
    # Assume first player in dict is you
    for p in state["players"].values():
        return p["pos"], p["alive"]
    return [MAP_CENTER[0], MAP_CENTER[1]], True

while True:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    send_input(keys)

    data = sock.recv(8192)
    state = pickle.loads(data)

    # Camera: center on player
    player_pos, you_alive = get_player_pos(state)
    cam_x = player_pos[0] - WIDTH // 2
    cam_y = player_pos[1] - HEIGHT // 2

    # Draw background grid for visual feedback
    screen.fill((220, 220, 220))
    for gx in range(-WIDTH, WIDTH*2, 40):
        pygame.draw.line(screen, (200, 200, 200), (gx - cam_x % 40, 0), (gx - cam_x % 40, HEIGHT))
    for gy in range(-HEIGHT, HEIGHT*2, 40):
        pygame.draw.line(screen, (200, 200, 200), (0, gy - cam_y % 40), (WIDTH, gy - cam_y % 40))

    # Draw circular map boundary
    circle_screen = (int(MAP_CENTER[0] - cam_x), int(MAP_CENTER[1] - cam_y))
    pygame.draw.circle(screen, (100, 100, 100), circle_screen, MAP_RADIUS, 4)

    # Draw flood (as a rectangle, but you could make it a circle if desired)
    flood_y = int(state["flood"] - cam_y)
    if 0 <= flood_y < HEIGHT:
        pygame.draw.rect(screen, (0, 100, 255), (0, flood_y, WIDTH, HEIGHT - flood_y))


    # Draw map (obstacles) with outline
    for obj in state["map"]:
        ox, oy, ow, oh = obj
        sx, sy = int(ox - cam_x), int(oy - cam_y)
        pygame.draw.rect(screen, (100, 100, 100), (sx, sy, ow, oh))
        pygame.draw.rect(screen, (180, 180, 180), (sx, sy, ow, oh), 2)

    # Draw weapons
    for w in state["weapons"]:
        wx, wy = int(w["x"] - cam_x), int(w["y"] - cam_y)
        pygame.draw.circle(screen, (255, 200, 0), (wx, wy), 5)

    # Draw bots
    # for bot in state["bots"]:
    #     if bot["alive"]:
    #         bx, by = int(bot["pos"][0] - cam_x), int(bot["pos"][1] - cam_y)
    #         pygame.draw.rect(screen, (255, 0, 0), (bx, by, 20, 20))


    # Draw players and count alive
    alive_count = 0
    for i, p in enumerate(state["players"].values()):
        if p["alive"]:
            alive_count += 1
            px, py = int(p["pos"][0] - cam_x), int(p["pos"][1] - cam_y)
            # Check if colliding with any box (for feedback)
            collides = False
            for obj in state["map"]:
                ox, oy, ow, oh = obj
                if px + 20 > int(ox - cam_x) and px < int(ox - cam_x) + ow and py + 20 > int(oy - cam_y) and py < int(oy - cam_y) + oh:
                    collides = True
                    break
            color = (255, 0, 0) if collides else (0, 255, 0)
            pygame.draw.rect(screen, color, (px, py, 20, 20))

    # Draw bullets
    for b in state["bullets"]:
        bx, by = int(b["pos"][0] - cam_x), int(b["pos"][1] - cam_y)
        pygame.draw.circle(screen, (0, 0, 0), (bx, by), 3)

    # HUD: show alive count
    hud = font.render(f"Players alive: {alive_count}", True, (0,0,0))
    screen.blit(hud, (10, 10))

    # Show death message if dead
    if not you_alive:
        if alive_last:
            death_timer = pygame.time.get_ticks()
        msg = font.render("You died! Press ESC to quit.", True, (200,0,0))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 20))
        # Optionally, freeze input or allow spectate
        # Wait for ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sock.close()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sock.close()
                exit()
        pygame.display.flip()
        alive_last = False
        continue
    else:
        alive_last = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sock.close()
            exit()

    pygame.display.flip()