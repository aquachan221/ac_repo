import pygame
import tkinter as tk
import numpy as np
import random

# Grid
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Simulation setup
NUM_AGENTS = 50
NUM_PLANTS = 100
MUTATION_RATE = 0.05
PLANT_REGROWTH = 10

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genivore Ecosystem")
clock = pygame.time.Clock()

grid = np.zeros((ROWS, COLS), dtype=int)  # 0 = empty, -1 = plant, 1+ = agent ID

agents = {}
species_stats = {}
next_species_id = 1

def random_traits():
    return {
        "speed": random.randint(1, 3),
        "aggression": random.randint(0, 10),
        "diet_memory": {"plants": 0, "meat": 0},
        "energy": 20,
        "diet": "omnivore",
        "lineage": next_species_id
    }

def spawn_agent(r=None, c=None):
    global next_species_id
    if r is None or c is None:
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    while grid[r, c] != 0:
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    traits = random_traits()
    aid = max(agents.keys(), default=0) + 1
    agents[aid] = {"pos": [r, c], **traits}
    grid[r, c] = aid
    if traits["lineage"] not in species_stats:
        species_stats[traits["lineage"]] = {"count": 0, "diet": traits["diet"], "aggression": traits["aggression"]}
        next_species_id += 1

def spawn_plant():
    for _ in range(PLANT_REGROWTH):
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if grid[r, c] == 0:
            grid[r, c] = -1

def move_agent(aid):
    agent = agents[aid]
    r, c = agent["pos"]
    dr, dc = random.randint(-agent["speed"], agent["speed"]), random.randint(-agent["speed"], agent["speed"])
    nr, nc = max(0, min(ROWS - 1, r + dr)), max(0, min(COLS - 1, c + dc))

    target = grid[nr, nc]
    if target == -1 and agent["diet"] in ["herbivore", "omnivore"]:
        agent["energy"] += 5
        agent["diet_memory"]["plants"] += 1
        grid[r, c] = 0
        grid[nr, nc] = aid
        agent["pos"] = [nr, nc]
    elif target > 0 and target != aid:
        other = agents.get(target)
        if other and agent["aggression"] > 5 and agent["diet"] in ["carnivore", "omnivore"]:
            agent["energy"] += 8
            agent["diet_memory"]["meat"] += 1
            grid[r, c] = 0
            grid[nr, nc] = aid
            agent["pos"] = [nr, nc]
            del agents[target]
        else:
            pass  # blocked
    elif target == 0:
        grid[r, c] = 0
        grid[nr, nc] = aid
        agent["pos"] = [nr, nc]

def evolve_agent(aid):
    global next_species_id  # ✅ Fix added

    agent = agents[aid]
    mem = agent["diet_memory"]
    total = mem["plants"] + mem["meat"]
    if total == 0: return
    plant_ratio = mem["plants"] / total
    meat_ratio = mem["meat"] / total

    if plant_ratio > 0.7:
        agent["diet"] = "herbivore"
    elif meat_ratio > 0.7:
        agent["diet"] = "carnivore"
    else:
        agent["diet"] = "omnivore"

    if random.random() < MUTATION_RATE:
        agent["lineage"] = next_species_id
        species_stats[next_species_id] = {
            "count": 0,
            "diet": agent["diet"],
            "aggression": agent["aggression"] + random.randint(-2, 2)
        }
        next_species_id += 1

def update_dashboard():
    root = tk.Tk()
    root.title("Genivore Species Overview")
    for sid, stats in species_stats.items():
        count = sum(1 for a in agents.values() if a["lineage"] == sid)
        diet = stats["diet"]
        aggression = stats["aggression"]
        label = tk.Label(root, text=f"Species {sid} | Count: {count} | Diet: {diet} | Aggression: {aggression}")
        label.pack()
    root.mainloop()

# Initialize world
for _ in range(NUM_PLANTS): spawn_plant()
for _ in range(NUM_AGENTS): spawn_agent()

# Main loop
running = True
while running:
    clock.tick(10)
    spawn_plant()

    for aid in list(agents.keys()):
        agent = agents.get(aid)  # ✅ Prevent KeyError
        if not agent:
            continue
        if agent["energy"] <= 0:
            r, c = agent["pos"]
            grid[r, c] = 0
            del agents[aid]
            continue
        move_agent(aid)
        agent["energy"] -= 1
        evolve_agent(aid)

    for sid in species_stats:
        species_stats[sid]["count"] = sum(1 for a in agents.values() if a["lineage"] == sid)

    # Draw grid
    screen.fill((0, 0, 0))
    for r in range(ROWS):
        for c in range(COLS):
            val = grid[r, c]
            if val == -1:
                pygame.draw.rect(screen, (0, 255, 0), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
            elif val > 0:
                agent = agents.get(val)
                if not agent:
                    continue
                color = {
                    "herbivore": (0, 150, 255),
                    "carnivore": (255, 50, 50),
                    "omnivore": (180, 180, 180),
                }[agent["diet"]]
                pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            update_dashboard()

pygame.quit()