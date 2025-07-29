import pygame
import numpy as np

# Grid setup
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
DEAD_COLOR = (10, 10, 10)
ALIVE_COLOR = (0, 200, 200)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Cell grid (0 = dead, 1 = alive)
grid = np.random.choice([0, 1], size=(ROWS, COLS))

def update(grid):
    new_grid = np.copy(grid)
    for r in range(ROWS):
        for c in range(COLS):
            alive_neighbors = np.sum(grid[r-1:r+2, c-1:c+2]) - grid[r, c]
            if grid[r, c] == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[r, c] = 0
            else:
                if alive_neighbors == 3:
                    new_grid[r, c] = 1
    return new_grid

def draw(grid):
    for r in range(ROWS):
        for c in range(COLS):
            color = ALIVE_COLOR if grid[r, c] == 1 else DEAD_COLOR
            pygame.draw.rect(screen, color,
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

# Main loop
running = True
while running:
    clock.tick(10)
    screen.fill(DEAD_COLOR)
    draw(grid)
    pygame.display.flip()
    grid = update(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            if 0 <= row < ROWS and 0 <= col < COLS:
                grid[row, col] = 1 - grid[row, col]  # Toggle cell state

pygame.quit()