import pygame
import sys
import subprocess
import socket

pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, GRAY, HOVER = (255,255,255), (0,0,0), (180,180,180), (100,100,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SSBBG Main Menu")
font = pygame.font.SysFont(None, 60)
input_font = pygame.font.SysFont(None, 40)

# States
MAIN_MENU = "main"
PLAY_MENU = "play"
JOIN_MENU = "join"
HOST_MENU = "host"
state = MAIN_MENU

main_buttons = [
    {"label": "Play", "rect": pygame.Rect(300, 200, 200, 60)},
    {"label": "Options", "rect": pygame.Rect(300, 300, 200, 60)},
    {"label": "Exit", "rect": pygame.Rect(300, 400, 200, 60)},
]

play_buttons = [
    {"label": "Host", "rect": pygame.Rect(300, 250, 200, 60)},
    {"label": "Join", "rect": pygame.Rect(300, 350, 200, 60)},
    {"label": "Back", "rect": pygame.Rect(300, 450, 200, 60)},
]

host_inputs = {"Server Name": "", "Max Players": "", "Password": ""}
input_boxes = []
active_box = None
join_buttons = []
host_launch_rect = None
host_back_rect = None

def scan_for_sessions():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.settimeout(1.5)
    try:
        udp.sendto(b"DISCOVER_SSBBG", ('<broadcast>', 54545))
    except:
        return []
    found = []
    try:
        while True:
            data, addr = udp.recvfrom(1024)
            msg = data.decode()
            parts = msg.split("|")
            if len(parts) == 3:
                found.append({"ip": parts[2], "info": f"{parts[0]} | {parts[1]}"})
    except socket.timeout:
        pass
    udp.close()
    return found

def draw_buttons(buttons, title_text):
    screen.fill(WHITE)
    title = font.render(title_text, True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        rect = button["rect"]
        pygame.draw.rect(screen, HOVER if rect.collidepoint(mouse_pos) else GRAY, rect)
        label = font.render(button["label"], True, BLACK)
        screen.blit(label, (rect.x + 30, rect.y + 10))

def draw_join_menu():
    screen.fill(WHITE)
    title = font.render("Join Game", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    mouse_pos = pygame.mouse.get_pos()
    for button in join_buttons:
        rect = button["rect"]
        pygame.draw.rect(screen, HOVER if rect.collidepoint(mouse_pos) else GRAY, rect)
        label = font.render(button["label"], True, BLACK)
        screen.blit(label, (rect.x + 20, rect.y + 5))
    back_rect = pygame.Rect(300, 500, 200, 50)
    pygame.draw.rect(screen, GRAY, back_rect)
    screen.blit(font.render("Back", True, BLACK), (back_rect.x + 50, back_rect.y + 5))
    return back_rect

def draw_host_menu():
    global host_launch_rect, host_back_rect
    screen.fill(WHITE)
    title = font.render("Host Game", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    global input_boxes
    input_boxes = []
    y_offset = 150
    for i, key in enumerate(host_inputs):
        label = input_font.render(f"{key}:", True, BLACK)
        screen.blit(label, (200, y_offset + i * 90))
        box = pygame.Rect(200, y_offset + i * 90 + 30, 400, 50)
        input_boxes.append((key, box))
        pygame.draw.rect(screen, HOVER if active_box == key else GRAY, box)
        text = input_font.render(host_inputs[key], True, BLACK)
        screen.blit(text, (box.x + 10, box.y + 10))
    host_launch_rect = pygame.Rect(250, 500, 140, 50)
    host_back_rect = pygame.Rect(430, 500, 140, 50)
    pygame.draw.rect(screen, GRAY, host_launch_rect)
    pygame.draw.rect(screen, GRAY, host_back_rect)
    screen.blit(font.render("Host", True, BLACK), (host_launch_rect.x + 30, host_launch_rect.y + 5))
    screen.blit(font.render("Back", True, BLACK), (host_back_rect.x + 30, host_back_rect.y + 5))

def main():
    global state, active_box
    while True:
        if state == MAIN_MENU:
            draw_buttons(main_buttons, "Game Menu")
        elif state == PLAY_MENU:
            draw_buttons(play_buttons, "Play Options")
        elif state == JOIN_MENU:
            back_rect = draw_join_menu()
        elif state == HOST_MENU:
            draw_host_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == MAIN_MENU:
                    for button in main_buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["label"] == "Play":
                                state = PLAY_MENU
                            elif button["label"] == "Options":
                                print("Options selected")  # Placeholder
                            elif button["label"] == "Exit":
                                pygame.quit(); sys.exit()

                elif state == PLAY_MENU:
                    for button in play_buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["label"] == "Host":
                                state = HOST_MENU
                            elif button["label"] == "Join":
                                join_buttons.clear()
                                sessions = scan_for_sessions()
                                for i, sess in enumerate(sessions):
                                    rect = pygame.Rect(200, 200 + i * 70, 400, 50)
                                    join_buttons.append({
                                        "label": sess["info"],
                                        "ip": sess["ip"],
                                        "rect": rect
                                    })
                                state = JOIN_MENU
                            elif button["label"] == "Back":
                                state = MAIN_MENU

                elif state == JOIN_MENU:
                    for button in join_buttons:
                        if button["rect"].collidepoint(event.pos):
                            ip = button["ip"]
                            subprocess.Popen(["python", "ssbbg_client.py", "--ip", ip])
                            state = MAIN_MENU
                    if back_rect.collidepoint(event.pos):
                        state = PLAY_MENU

                elif state == HOST_MENU:
                    for key, box in input_boxes:
                        if box.collidepoint(event.pos):
                            active_box = key
                    if host_launch_rect and host_launch_rect.collidepoint(event.pos):
                        args = ["python", "ssbbg_server.py", "--name", host_inputs["Server Name"], "--max", host_inputs["Max Players"]]
                        if host_inputs["Password"]:
                            args += ["--password", host_inputs["Password"]]
                        subprocess.Popen(args)
                        state = MAIN_MENU
                    if host_back_rect and host_back_rect.collidepoint(event.pos):
                        active_box = None
                        state = PLAY_MENU

            elif event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    host_inputs[active_box] = host_inputs[active_box][:-1]
                elif event.key == pygame.K_RETURN:
                    active_box = None
                else:
                    host_inputs[active_box] += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
    main()