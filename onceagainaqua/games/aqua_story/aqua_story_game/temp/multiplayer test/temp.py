import pygame
import socket
import json

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

SERVER_IP = "192.168.1.108"
SERVER_PORT = 50000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

running = True
while running:
    screen.fill((30, 30, 30))

    pygame.event.get()
    keys = pygame.key.get_pressed()
    move_direction = ""
    if keys[pygame.K_w]: move_direction = "W"
    if keys[pygame.K_s]: move_direction = "S"
    if keys[pygame.K_a]: move_direction = "A"
    if keys[pygame.K_d]: move_direction = "D"

    client.send(f"MOVE {move_direction}".encode())

    # Receive data from server
    data = client.recv(1024).decode()
    
    print(f"Received raw data: {data}")  # Debugging log

    positions = {}  # Always define positions to prevent NameError

    if data:  # Ensure it's non-empty before decoding
        try:
            positions = json.loads(data)
        except json.JSONDecodeError:
            print("Error: Received invalid JSON data.")
            positions = {}  # Prevent crashes

    for player, pos in positions.items():
        pygame.draw.rect(screen, (255, 255, 0), (pos["x"], pos["y"], 20, 20))

    pygame.display.flip()
    pygame.time.delay(30)