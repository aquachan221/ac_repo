import socket
import pickle
import argparse
import pygame

# --- Setup ---
parser = argparse.ArgumentParser()
parser.add_argument("--ip", required=True)
args = parser.parse_args()

HOST = args.ip
PORT = 5555
WIDTH, HEIGHT = 800, 600
WHITE, RED, BLUE, BLACK = (255,255,255), (255,0,0), (0,0,255), (0,0,0)
PLAYER_RADIUS = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SSBBG Client")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Connect ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    print("[❌] Could not connect to server.")
    exit()

start_data = pickle.loads(client.recv(4096))
player_id = start_data["id"]
x, y = start_data["base"]
bullets = []
score = 0
alive = True

# --- Game Loop ---
run = True
while run:
    clock.tick(60)
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dir_vector = pygame.math.Vector2(mouse_x - x, mouse_y - y)
    if dir_vector.length() > 0:
        dir_vector = dir_vector.normalize()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: y -= 5
    if keys[pygame.K_s]: y += 5
    if keys[pygame.K_a]: x -= 5
    if keys[pygame.K_d]: x += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and alive:
            bullets.append([x, y, dir_vector])

    # Move bullets
    for b in bullets:
        b[0] += b[2].x * 10
        b[1] += b[2].y * 10
        pygame.draw.circle(screen, BLACK, (int(b[0]), int(b[1])), 5)

    # Send state to server
    send_data = {"x": x, "y": y, "bullets": bullets, "alive": alive, "score": score}
    try:
        client.send(pickle.dumps(send_data))
        players = pickle.loads(client.recv(4096))
    except:
        print("[⚠️] Lost connection to server.")
        break

    # Sync position and score
    new_x, new_y = players[player_id].get("x", x), players[player_id].get("y", y)
    if (new_x, new_y) != (x, y):
        x, y = new_x, new_y
        bullets = []

    score = players[player_id].get("score", 0)
    alive = players[player_id].get("alive", True)

    # Draw all players
    for i, p in enumerate(players):
        color = BLUE if i == player_id else RED
        px, py = int(p.get("x", 0)), int(p.get("y", 0))
        pygame.draw.circle(screen, color, (px, py), PLAYER_RADIUS)
        label = font.render(f"P{i} Score: {p.get('score', 0)}", True, BLACK)
        screen.blit(label, (10, 10 + i * 30))

    pygame.display.flip()

pygame.quit()