import pygame # type: ignore
import numpy as np # type: ignore
import sys

# Game settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 60
TRAIL_COLOR = (255, 255, 0)
TERRITORY_COLOR = (0, 200, 255)
PLAYER_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)
FONT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper.io Lite - Grid Based")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_territory(mask):
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.set_colorkey((0, 0, 0))
    surf.fill((0, 0, 0))
    surf.blit(mask, (0, 0))
    screen.blit(surf, (0, 0))

def draw_trail(trail):
    for gx, gy in trail:
        pygame.draw.rect(screen, TRAIL_COLOR, (gx * CELL_SIZE, gy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(gpos):
    pygame.draw.rect(screen, PLAYER_COLOR, (gpos[0] * CELL_SIZE, gpos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, FONT_COLOR)
    screen.blit(text, (10, 10))

def fill_polygon(mask, trail):
    if len(trail) < 3:
        return 0
    poly = [(gx * CELL_SIZE + CELL_SIZE // 2, gy * CELL_SIZE + CELL_SIZE // 2) for gx, gy in trail]
    pygame.draw.polygon(mask, TERRITORY_COLOR, poly)
    arr = pygame.surfarray.array3d(mask).transpose(2, 1, 0)  # shape: (3, HEIGHT, WIDTH)
    # Count pixels matching TERRITORY_COLOR
    area = np.all(arr == np.array(TERRITORY_COLOR).reshape(3, 1, 1), axis=0).sum()
    return area

def point_in_territory(mask, gpos):
    x = gpos[0] * CELL_SIZE + CELL_SIZE // 2
    y = gpos[1] * CELL_SIZE + CELL_SIZE // 2
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        return mask.get_at((x, y))[:3] == TERRITORY_COLOR
    return False

def main():
    # Start in the center with a small square territory
    start_gx = GRID_WIDTH // 2
    start_gy = GRID_HEIGHT // 2
    player_gpos = [start_gx, start_gy]
    direction = [0, 0]
    mask = pygame.Surface((WIDTH, HEIGHT))
    # Initial territory: 4x4 square
    for gx in range(start_gx - 2, start_gx + 2):
        for gy in range(start_gy - 2, start_gy + 2):
            pygame.draw.rect(mask, TERRITORY_COLOR, (gx * CELL_SIZE, gy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    arr = pygame.surfarray.array3d(mask).transpose(2, 1, 0)  # shape: (3, HEIGHT, WIDTH)
    score = np.all(arr == np.array(TERRITORY_COLOR).reshape(3, 1, 1), axis=0).sum()
    trail = []
    in_trail = False
    move_cooldown = 0

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Grid-based movement: only move on keydown
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    direction = [1, 0]
                elif event.key == pygame.K_UP:
                    direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    direction = [0, 1]

        # Move player (one cell per frame if direction is set)
        if direction != [0, 0] and move_cooldown == 0:
            new_gx = player_gpos[0] + direction[0]
            new_gy = player_gpos[1] + direction[1]
            if 0 <= new_gx < GRID_WIDTH and 0 <= new_gy < GRID_HEIGHT:
                player_gpos = [new_gx, new_gy]
                move_cooldown = 5  # frames between moves

        if move_cooldown > 0:
            move_cooldown -= 1

        # Check if player is on territory
        on_territory = point_in_territory(mask, player_gpos)

        if not on_territory:
            if not in_trail:
                trail = []
                in_trail = True
            # Only add new positions if moved
            if not trail or tuple(player_gpos) != trail[-1]:
                trail.append(tuple(player_gpos))
        else:
            if in_trail and len(trail) > 2:
                score = fill_polygon(mask, trail)
                trail = []
            in_trail = False

        # Draw everything
        draw_territory(mask)
        draw_trail(trail)
        draw_player(player_gpos)
        draw_score(score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()