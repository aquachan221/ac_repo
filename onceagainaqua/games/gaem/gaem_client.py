# client.py

import pygame
import socket
import pickle
import threading

HOST = '192.168.1.78'  # Replace with server IP
PORT = 5555

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Dot Game")
clock = pygame.time.Clock()
FPS = 60



# Each player is a snake: list of segments [[x, y], ...]
snake = [[100, 100], [90, 100], [80, 100], [70, 100], [60, 100]]
others = {}  # cid -> snake
food = []

# Infinite map size (match server)
MAP_WIDTH, MAP_HEIGHT = 2000, 2000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def receive_updates():
    global others, food
    while True:
        try:
            update = sock.recv(4096)
            if update:
                msg = pickle.loads(update)
                # msg: {'snakes': {cid: snake}, 'food': [[x, y], ...]}
                others = msg['snakes']
                food = msg['food']
        except:
            break

threading.Thread(target=receive_updates, daemon=True).start()


def send_snake():
    data = pickle.dumps({'snake': snake})
    sock.sendall(data)



def move_snake_towards_mouse(snake, speed=3):
    if not snake:
        return
    mx, my = pygame.mouse.get_pos()
    # Camera is centered on head, so mouse is relative to center
    hx, hy = snake[0]
    cam_x = hx - WIDTH // 2
    cam_y = hy - HEIGHT // 2
    world_mx = cam_x + mx
    world_my = cam_y + my
    dx, dy = world_mx - hx, world_my - hy
    dist = (dx**2 + dy**2) ** 0.5
    if dist == 0:
        return
    dx, dy = dx / dist, dy / dist
    new_head = [hx + dx * speed, hy + dy * speed]
    # Clamp to map bounds (optional, or allow infinite)
    # new_head[0] = max(0, min(MAP_WIDTH, new_head[0]))
    # new_head[1] = max(0, min(MAP_HEIGHT, new_head[1]))
    # Move body
    prev = list(new_head)
    for i in range(len(snake)):
        tmp = list(snake[i])
        snake[i] = prev
        prev = tmp


def check_eat_food():
    global food, snake
    head = snake[0]
    for f in food:
        if abs(head[0] - f[0]) < 15 and abs(head[1] - f[1]) < 15:
            # Grow snake by duplicating last segment
            snake.append(list(snake[-1]))
            return True
    return False


running = True
while running:
    clock.tick(FPS)
    # Fill background with dark gray
    screen.fill((30, 30, 30))

    # Camera offset: center on head
    hx, hy = snake[0]
    cam_x = hx - WIDTH // 2
    cam_y = hy - HEIGHT // 2

    # Draw grid of small light gray dots to show movement
    grid_spacing = 40
    dot_color = (80, 80, 80)
    dot_radius = 2
    # Find top-left world coordinate visible
    start_x = cam_x - (cam_x % grid_spacing) - grid_spacing
    start_y = cam_y - (cam_y % grid_spacing) - grid_spacing
    for gx in range(start_x, cam_x + WIDTH + grid_spacing, grid_spacing):
        for gy in range(start_y, cam_y + HEIGHT + grid_spacing, grid_spacing):
            sx, sy = int(gx - cam_x), int(gy - cam_y)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                pygame.draw.circle(screen, dot_color, (sx, sy), dot_radius)

    move_snake_towards_mouse(snake)
    # Check if we ate food (let server handle respawn, but grow locally for smoothness)
    if check_eat_food():
        pass
    send_snake()

    # Draw food
    for fx, fy in food:
        sx, sy = int(fx - cam_x), int(fy - cam_y)
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            pygame.draw.circle(screen, (255, 0, 0), (sx, sy), 7)

    # Draw all snakes and offscreen indicators
    for cid, s in others.items():
        if s == snake:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        # Draw snake segments if on screen
        onscreen = False
        for seg in s:
            sx, sy = int(seg[0] - cam_x), int(seg[1] - cam_y)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                pygame.draw.rect(screen, color, (sx, sy, 12, 12))
                onscreen = True
        # If not onscreen, draw indicator for head
        head = s[0]
        sx, sy = int(head[0] - cam_x), int(head[1] - cam_y)
        if not (0 <= sx < WIDTH and 0 <= sy < HEIGHT):
            # Find direction from center to head
            cx, cy = WIDTH // 2, HEIGHT // 2
            dx, dy = sx - cx, sy - cy
            if dx == 0 and dy == 0:
                continue
            import math
            angle = math.atan2(dy, dx)
            # Find intersection with screen edge
            # Parametric line from center (cx,cy) in direction (dx,dy)
            # Find t where it hits one of the 4 edges
            t_vals = []
            if dx != 0:
                t_left = (0 - cx) / dx
                t_right = (WIDTH - 1 - cx) / dx
                t_vals.extend([t_left, t_right])
            if dy != 0:
                t_top = (0 - cy) / dy
                t_bottom = (HEIGHT - 1 - cy) / dy
                t_vals.extend([t_top, t_bottom])
            t_edge = min([t for t in t_vals if t > 0], default=1)
            ex = int(cx + dx * t_edge)
            ey = int(cy + dy * t_edge)
            # Clamp to screen
            ex = max(0, min(WIDTH - 1, ex))
            ey = max(0, min(HEIGHT - 1, ey))
            pygame.draw.circle(screen, color, (ex, ey), 10)

    # Draw own snake on top
    for seg in snake:
        sx, sy = int(seg[0] - cam_x), int(seg[1] - cam_y)
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            pygame.draw.rect(screen, (0, 200, 0), (sx, sy, 12, 12))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sock.close()